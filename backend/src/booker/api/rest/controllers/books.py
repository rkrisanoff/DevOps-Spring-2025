from typing import Any, Annotated
from uuid import UUID

from litestar import Controller, get, post, put, patch, delete
from litestar.dto import DataclassDTO, DTOConfig, DTOData
from litestar.pagination import OffsetPagination
from litestar.params import Parameter, Dependency
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass, field

from booker.domain.models import Book
from booker.domain.entities import BookGenre


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


# DTO по современной документации Litestar
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
    async def get_books(
        self,
        session: AsyncSession,
        offset: int = Parameter(default=0, ge=0, description="Начальный индекс для пагинации"),
        limit: int = Parameter(default=10, ge=1, le=100, description="Максимальное количество элементов на странице"),
    ) -> OffsetPagination[BookDTO]:
        query = select(Book)
        
        # Выполняем запрос с учетом пагинации
        result = await session.execute(
            query.limit(limit).offset(offset)
        )
        items = result.scalars().all()
        
        # Выполняем запрос для подсчета общего количества
        count_result = await session.execute(select(Book))
        total = len(count_result.scalars().all())
        
        # Формируем ответ с пагинацией
        return OffsetPagination[BookDTO](
            items=[BookDTO(
                id=item.id,
                title=item.title,
                author=item.author,
                genres=item.genres,
                year=item.year,
                language=item.language,
                pages=item.pages,
                status=item.status
            ) for item in items],
            total=total,
            limit=limit,
            offset=offset,
        )

    @get("/{book_id:int}")
    async def get_book(
        self, 
        session: AsyncSession, 
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги")
    ) -> BookDTO:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        book = result.scalar_one_or_none()
        
        if book is None:
            raise HTTPException(
                status_code=404,
                detail=f"Книга с ID {book_id} не найдена"
            )
        
        return BookDTO(
            id=book.id,
            title=book.title,
            author=book.author,
            genres=book.genres,
            year=book.year,
            language=book.language,
            pages=book.pages,
            status=book.status
        )

    @post(dto=BookWriteDTO)
    async def create_book(
        self, 
        session: AsyncSession, 
        data: DTOData[BookDTO]
    ) -> BookDTO:
        try:
            book = Book(**data.as_builtins())
            
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
                status=book.status
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    @patch("/{book_id:int}", dto=BookPatchDTO)
    async def update_book(
        self, 
        session: AsyncSession, 
        data: DTOData[BookDTO],
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги")
    ) -> BookDTO:
        query = select(Book).where(Book.id.__eq__(book_id))
        result = await session.execute(query)
        book = result.scalar_one_or_none()
        
        if book is None:
            raise HTTPException(
                status_code=404,
                detail=f"Книга с ID {book_id} не найдена"
            )
        
        # Обновляем только предоставленные поля
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
            status=book.status
        )

    @delete("/{book_id:int}")
    async def delete_book(
        self, 
        session: AsyncSession, 
        book_id: int = Parameter(title="ID книги", description="Уникальный идентификатор книги")
    ) -> None:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        book = result.scalar_one_or_none()
        
        if book is None:
            raise HTTPException(
                status_code=404,
                detail=f"Книга с ID {book_id} не найдена"
            )
        
        await session.delete(book)
        await session.commit()
