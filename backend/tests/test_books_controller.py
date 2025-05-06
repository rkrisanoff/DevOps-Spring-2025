from collections.abc import AsyncGenerator
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from litestar import Litestar
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from booker.api.rest.controllers.books import BooksController
from booker.domain.entities import Status
from booker.domain.models import Book, BookGenre
from booker.settings import EmbedderConfig, WebServerConfig


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def mock_config():
    config = MagicMock(spec=WebServerConfig)
    config.embedder = MagicMock(spec=EmbedderConfig)
    config.embedder.endpoint = "http://test-embedder"
    return config


@pytest.fixture
def app(mock_session, mock_config) -> Litestar:
    # Создаем зависимость для сессии
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        yield mock_session

    app = Litestar(
        route_handlers=[BooksController],
        dependencies={"session": get_session, "config": lambda: mock_config},
    )

    return app


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def test_book():
    return Book(
        id=1,
        title="Test Book",
        author="Test Author",
        genres=[BookGenre.FICTION],
        year=2024,
        language="English",
        pages=250,
        status=Status.TODO,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def test_books():
    return [
        Book(
            id=i,
            title=f"Test Book {i}",
            author=f"Test Author {i}",
            genres=[BookGenre.FICTION],
            year=2024,
            language="English",
            pages=250,
            status=Status.TODO,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for i in range(1, 4)
    ]


@pytest.mark.asyncio
async def test_get_books(client: TestClient, mock_session, test_books):
    # Arrange
    result = MagicMock()
    result.scalars.return_value.all.return_value = test_books
    mock_session.execute.return_value = result

    # Act
    response = client.get("/books")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 3
    assert data["limit"] == 10
    assert data["offset"] == 0
    assert data["items"][0]["title"] == "Test Book 1"
    assert data["items"][1]["title"] == "Test Book 2"
    assert data["items"][2]["title"] == "Test Book 3"


@pytest.mark.asyncio
async def test_get_books_pagination(client: TestClient, mock_session, test_books):
    # Arrange
    result = MagicMock()
    result.scalars.return_value.all.side_effect = [
        test_books[:2],
        test_books,
    ]  # Первый вызов - первые 2 книги, второй - все
    mock_session.execute.return_value = result

    # Act
    response = client.get("/books?offset=0&limit=2")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["limit"] == 2
    assert data["offset"] == 0
    assert data["items"][0]["title"] == "Test Book 1"
    assert data["items"][1]["title"] == "Test Book 2"


@pytest.mark.asyncio
async def test_get_book(client: TestClient, mock_session, test_book):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = test_book
    mock_session.execute.return_value = result

    # Act
    response = client.get(f"/books/{test_book.id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_book.id
    assert data["title"] == test_book.title
    assert data["author"] == test_book.author
    assert data["genres"] == [genre.value for genre in test_book.genres]
    assert data["year"] == test_book.year
    assert data["language"] == test_book.language
    assert data["pages"] == test_book.pages
    assert data["status"] == test_book.status


@pytest.mark.asyncio
async def test_get_book_not_found(client: TestClient, mock_session):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = result

    # Act
    response = client.get("/books/999")

    # Assert
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


# @pytest.mark.asyncio
# async def test_create_book(client: TestClient, mock_session, mock_config):
#     # Arrange
#     book_data = {
#         "title": "New Book",
#         "author": "New Author",
#         "genres": [BookGenre.FICTION.value],
#         "year": 2024,
#         "language": "English",
#         "pages": 250,
#         "status": Status.TODO.value,
#     }

#     # Mock DTOData
#     mock_dto = MagicMock()
#     mock_dto.as_builtins.return_value = book_data

#     # Mock session operations
#     mock_session.add = AsyncMock()
#     mock_session.commit = AsyncMock()
#     mock_session.refresh = AsyncMock()

#     # Mock embedding service response
#     mock_response = MagicMock()
#     mock_response.ok = True
#     mock_response.json.return_value = [[0.1, 0.2, 0.3]]

#     with patch("booker.api.rest.controllers.books.requests.get", return_value=mock_response), \
#          patch("booker.api.rest.controllers.books.DTOData", return_value=mock_dto):
#         # Act
#         response = client.post("/books", json=book_data)

#         # Assert
#         assert response.status_code == 201
#         data = response.json()
#         assert data["title"] == book_data["title"]
#         assert data["author"] == book_data["author"]
#         assert data["genres"] == book_data["genres"]
#         assert data["year"] == book_data["year"]
#         assert data["language"] == book_data["language"]
#         assert data["pages"] == book_data["pages"]
#         assert data["status"] == book_data["status"]
#         assert mock_session.add.called
#         assert mock_session.commit.called
#         assert mock_session.refresh.called


@pytest.mark.asyncio
async def test_create_book_error(client: TestClient, mock_session, mock_config):
    # Arrange
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock(side_effect=Exception("Database error"))
    mock_session.rollback = AsyncMock()

    book_data = {
        "title": "New Book",
        "author": "New Author",
        "genres": [BookGenre.FICTION.value],
        "year": 2024,
        "language": "English",
        "pages": 250,
        "status": Status.TODO.value,
    }

    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = [[0.1, 0.2, 0.3]]
    mock_config.embedder.endpoint = "http://test-embedder"

    with patch("booker.api.rest.controllers.books.requests.get", return_value=mock_response):
        response = client.post("/books", json=book_data)

        assert response.status_code == 500
        assert "Internal Server Error" in response.json()["detail"]
        assert not mock_session.refresh.called


@pytest.mark.asyncio
async def test_update_book(client: TestClient, mock_session, test_book):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = test_book
    mock_session.execute.return_value = result

    # После обновления возвращаем обновленную книгу
    updated_book = Book(
        id=test_book.id,
        title="Updated Title",
        author=test_book.author,
        genres=test_book.genres,
        year=test_book.year,
        language=test_book.language,
        pages=test_book.pages,
        status=test_book.status,
        created_at=test_book.created_at,
        updated_at=test_book.updated_at,
    )
    mock_session.refresh.return_value = updated_book

    update_data = {"title": "Updated Title"}

    # Act
    response = client.patch(f"/books/{test_book.id}", json=update_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_book.id
    assert data["title"] == "Updated Title"
    assert data["author"] == test_book.author
    assert data["genres"] == [genre.value for genre in test_book.genres]
    assert data["year"] == test_book.year
    assert data["language"] == test_book.language
    assert data["pages"] == test_book.pages
    assert data["status"] == test_book.status
    assert mock_session.commit.called
    assert mock_session.refresh.called


@pytest.mark.asyncio
async def test_update_book_all_fields(client: TestClient, mock_session, test_book):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = test_book
    mock_session.execute.return_value = result

    # После обновления возвращаем обновленную книгу
    updated_book = Book(
        id=test_book.id,
        title="Updated Title",
        author="Updated Author",
        genres=[BookGenre.FANTASY, BookGenre.MYSTERY],
        year=2025,
        language="Russian",
        pages=300,
        status=Status.READING,
        created_at=test_book.created_at,
        updated_at=test_book.updated_at,
    )
    mock_session.refresh.return_value = updated_book

    update_data = {
        "title": "Updated Title",
        "author": "Updated Author",
        "genres": [BookGenre.FANTASY.value, BookGenre.MYSTERY.value],
        "year": 2025,
        "language": "Russian",
        "pages": 300,
        "status": Status.READING.value,
    }

    # Act
    response = client.patch(f"/books/{test_book.id}", json=update_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_book.id
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"
    assert data["genres"] == [BookGenre.FANTASY.value, BookGenre.MYSTERY.value]
    assert data["year"] == 2025
    assert data["language"] == "Russian"
    assert data["pages"] == 300
    assert data["status"] == Status.READING.value
    assert mock_session.commit.called
    assert mock_session.refresh.called


@pytest.mark.asyncio
async def test_update_book_not_found(client: TestClient, mock_session):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = result

    update_data = {"title": "Updated Title"}

    # Act
    response = client.patch("/books/999", json=update_data)

    # Assert
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_book(client: TestClient, mock_session, test_book):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = test_book
    mock_session.execute.return_value = result

    # Act
    response = client.delete(f"/books/{test_book.id}")

    # Assert
    assert response.status_code == 204
    assert mock_session.delete.called
    assert mock_session.commit.called


@pytest.mark.asyncio
async def test_delete_book_not_found(client: TestClient, mock_session):
    # Arrange
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = result

    # Act
    response = client.delete("/books/999")

    # Assert
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]
