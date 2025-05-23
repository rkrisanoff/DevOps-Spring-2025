from dataclasses import dataclass
from typing import Any

import requests
import requests.api
from aiokafka import AIOKafkaProducer
from litestar import Controller, delete, get, patch, post
from litestar.dto import DataclassDTO, DTOConfig, DTOData
from litestar.exceptions import HTTPException
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from booker.domain.entities import BookGenre, book_genre_map
from booker.domain.models import Book
from booker.service.book import BookService
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

    @post(dto=BookWriteDTO)
    async def create_book(
        self,
        config: WebServerConfig,
        session: AsyncSession,
        producer: AIOKafkaProducer,
        data: DTOData[BookDTO],
    ) -> BookDTO:
        try:
            book = Book(**data.as_builtins())
            relevant_representation = f"""{book.title} was written by {book.author} in {book.year} on {book.language}.
                Genres are {" ".join([book_genre_map.get(genre, genre) for genre in book.genres])}"""
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
            await producer.send_and_wait(
                topic="notifications",
                value={
                    "event_type": "create",
                    "payload": data.as_builtins(),
                },
            )

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
            raise HTTPException(status_code=500, detail=str(e)) from e

    @patch("/{book_id:int}", dto=BookPatchDTO)
    async def update_book(
        self,
        session: AsyncSession,
        producer: AIOKafkaProducer,
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
        await producer.send_and_wait(
            topic="notifications",
            value={
                "event_type": "update",
                "payload": update_data,
            },
        )

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
        producer: AIOKafkaProducer,
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

        await producer.send_and_wait(
            topic="notifications",
            value={
                "event_type": "delete",
                "payload": {"book_id": book_id},
            },
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

        similar_books = await BookService.get_similar(
            book_id=book_id, limit=limit, offset=offset, session=session
        )

        count_result = await session.execute(select(Book))
        total = len(count_result.scalars().all()) - 1

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
            "similar_books": similar_books,
            "limit": limit,
            "offset": offset,
            "total": total,
        }

    @post("/similar", dto=BookWriteDTO)
    async def similarify(
        self,
        config: WebServerConfig,
        session: AsyncSession,
        data: DTOData[BookDTO],
        offset: int = Parameter(default=0, ge=0, description="Начальный индекс для пагинации"),
        limit: int = Parameter(
            default=10, ge=1, description="Максимальное количество элементов на странице"
        ),
    ) -> list[dict[str, Any]]:
        book = Book(**data.as_builtins())
        relevant_representation = f"""{book.title} was written by {book.author} in {book.year} on {book.language}.
            Genres are {" ".join([book_genre_map.get(genre, genre) for genre in book.genres])}"""
        response = requests.get(
            f"{config.embedder.endpoint}/api/v1/infer/embedding",
            params={"sentences": [relevant_representation]},
        )
        if not response.ok:
            raise HTTPException(status_code=503, detail="Embedder service unavailable") from None

        embedding = response.json()[0]

        similar_books = await BookService.similarify(
            book_embedding=embedding, limit=limit, offset=offset, session=session
        )

        count_result = await session.execute(select(Book))
        total = len(count_result.scalars().all()) - 1

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
            "similar_books": similar_books,
            "limit": limit,
            "offset": offset,
            "total": total,
        }
