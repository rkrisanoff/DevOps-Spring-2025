from dataclasses import dataclass
from typing import Any

import requests
import requests.api
import sqlalchemy
from litestar import Controller, delete, get, patch, post
from litestar.dto import DataclassDTO, DTOConfig, DTOData
from litestar.exceptions import HTTPException
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from booker.domain.entities import BookGenre
from booker.domain.models import Book
from booker.settings import WebServerConfig


@dataclass
class BookDTO:
    title: str
    author: str
    genres: list[BookGenre]
    year: int
    language: str
    pages: int
    status: str
    id: int


class BookSimilarDTO(DataclassDTO[BookDTO]):
    config = DTOConfig(
        exclude={
            "status",
        }
    )


class BookReadDTO(DataclassDTO[BookDTO]):
    config = DTOConfig()


class BookWriteDTO(DataclassDTO[BookDTO]):
    config = DTOConfig(exclude={"id"})


class BookPatchDTO(DataclassDTO[BookDTO]):
    config = DTOConfig(exclude={"id"}, partial=True)


class BooksController(Controller):
    path = "/books"
    tags = ("Books",)
    return_dto = BookReadDTO

    @get()
    async def list_books(
        self,
        session: AsyncSession,
        offset: int = Parameter(default=0, ge=0, description="Начальный индекс для пагинации"),
        limit: int = Parameter(
            default=10, ge=1, le=100, description="Максимальное количество элементов на странице"
        ),
    ) -> OffsetPagination[BookDTO]:
        query = select(Book)

        result = await session.execute(query.limit(limit).offset(offset))
        items = result.scalars().all()

        count_result = await session.execute(select(Book))
        total = len(count_result.scalars().all())

        return OffsetPagination[BookDTO](
            items=[
                BookDTO(
                    id=item.id,
                    title=item.title,
                    author=item.author,
                    genres=item.genres,
                    year=item.year,
                    language=item.language,
                    pages=item.pages,
                    status=item.status,
                )
                for item in items
            ],
            total=total,
            limit=limit,
            offset=offset,
        )

    @get("/{book_id:int}")
    async def get_book(
        self,
        session: AsyncSession,
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги"),
    ) -> BookDTO:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        book = result.scalar_one_or_none()

        if book is None:
            raise HTTPException(
                status_code=404, detail=f"Книга с ID {book_id} не найдена"
            ) from None

        return BookDTO(
            id=book.id,
            title=book.title,
            author=book.author,
            genres=book.genres,
            year=book.year,
            language=book.language,
            pages=book.pages,
            status=book.status,
        )

    @get("/{book_id:int}/similar")
    async def get_similaris(
        self,
        session: AsyncSession,
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги"),
        offset: int = Parameter(default=0, ge=0, description="Начальный индекс для пагинации"),
        limit: int = Parameter(
            default=10, ge=1, description="Максимальное количество элементов на странице"
        ),
    ) -> list[dict[str, Any]]:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        book = result.scalar_one_or_none()

        if book is None:
            raise HTTPException(
                status_code=404, detail=f"Книга с ID {book_id} не найдена"
            ) from None

        query = sqlalchemy.text("""
WITH target_book_embedding AS (
    SELECT
        embedding AS reference_embedding
    FROM
        book
    WHERE
        id = :book_id
)

SELECT
    main_book.id                     AS id,
    main_book.title                  AS title,
    main_book.author                 AS author,
    main_book.genres                 AS genres,
    main_book.pages                  AS pages,
    main_book.year                   AS publication_year,
    1 - (main_book.embedding <=> target_book_embedding.reference_embedding) AS similarity
FROM
    book AS main_book

CROSS JOIN
    target_book_embedding
WHERE main_book.id != :book_id
ORDER BY
    similarity DESC
LIMIT :limit
OFFSET :offset
;
""")
        result = await session.execute(
            query,
            {
                "book_id": book_id,
                "limit": limit,
                "offset": offset,
            },
        )
        return {
            "target_book": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genres": book.genres,
                "year": book.year,
                "language": book.language,
                "pages": book.pages,
            },
            "similar_books": [row._asdict() for row in result],
        }

    @post(dto=BookWriteDTO)
    async def create_book(
        self, config: WebServerConfig, session: AsyncSession, data: DTOData[BookDTO]
    ) -> BookDTO:
        try:
            book = Book(**data.as_builtins())

            # Да, это кринж, но это +- приблизительно работает
            relevant_representation = f"""{book.title} was written by {book.author} in {book.year} on {book.language}.
                Genres are {" ".join(book.genres)}"""

            response = requests.get(
                f"{config.embedder.endpoint}/api/v1/infer/embedding",
                params={"sentences": [relevant_representation]},
            )
            if not response.ok:
                raise HTTPException(
                    status_code=503, detail="Embedder service unavailable"
                ) from None

            embedding = response.json()[0]
            book.embedding = embedding

            session.add(book)
            await session.commit()
            await session.refresh(book)

            return BookDTO(
                id=book.id,
                title=book.title,
                author=book.author,
                genres=book.genres,
                year=book.year,
                language=book.language,
                pages=book.pages,
                status=book.status,
            )

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e)) from None

    @patch("/{book_id:int}", dto=BookPatchDTO)
    async def update_book(
        self,
        session: AsyncSession,
        data: DTOData[BookDTO],
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги"),
    ) -> BookDTO:
        query = select(Book).where(Book.id.__eq__(book_id))
        result = await session.execute(query)
        book = result.scalar_one_or_none()

        if book is None:
            raise HTTPException(
                status_code=404, detail=f"Книга с ID {book_id} не найдена"
            ) from None

        update_data = data.as_builtins()
        for field, value in update_data.items():
            if value is not None:
                setattr(book, field, value)

        await session.commit()
        await session.refresh(book)

        return BookDTO(
            id=book.id,
            title=book.title,
            author=book.author,
            genres=book.genres,
            year=book.year,
            language=book.language,
            pages=book.pages,
            status=book.status,
        )

    @delete("/{book_id:int}")
    async def delete_book(
        self,
        session: AsyncSession,
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги"),
    ) -> None:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        book = result.scalar_one_or_none()

        if book is None:
            raise HTTPException(
                status_code=404, detail=f"Книга с ID {book_id} не найдена"
            ) from None

        await session.delete(book)
        await session.commit()
