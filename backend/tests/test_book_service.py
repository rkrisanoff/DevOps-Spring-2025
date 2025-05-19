from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from booker.service.book import BookService


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.mark.asyncio
async def test_get_similar_books(mock_session):
    # Arrange
    mock_result = MagicMock()
    mock_result._asdict.return_value = {"id": 2, "title": "Test Book", "similarity": 0.85}
    mock_session.execute.return_value = [mock_result]

    # Act
    result = await BookService.get_similar(book_id=1, limit=1, offset=0, session=mock_session)

    # Assert
    assert len(result) == 1
    assert result[0]["id"] == 2
    assert result[0]["similarity"] == 0.85


@pytest.mark.asyncio
async def test_get_similar_books_empty(mock_session):
    # Arrange
    mock_session.execute.return_value = []

    # Act
    result = await BookService.get_similar(book_id=1, limit=10, offset=0, session=mock_session)

    # Assert
    assert len(result) == 0
