import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import orjson
import pytest

# Устанавливаем тестовые переменные окружения
os.environ["BOT_TOKEN"] = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
os.environ["BOT_BACKEND_HOST"] = "backend"
os.environ["BOT_BACKEND_PORT"] = "8000"
os.environ["BOT_BROKER_HOST"] = "kafka"
os.environ["BOT_BROKER_PORT"] = "9092"
os.environ["BOT_NOTIFICATION_TARGET_CHAT_ID"] = "-4904260504"

# Мокируем создание бота перед импортом модуля
with patch("aiogram.Bot"):
    from bot.bot import wait_and_send_notifications


@pytest.fixture
def mock_consumer():
    """Фикстура для создания мока Kafka консьюмера"""
    consumer = AsyncMock()
    consumer.start = AsyncMock()
    consumer.stop = AsyncMock()
    return consumer


@pytest.fixture
def mock_bot():
    """Фикстура для создания мока бота"""
    bot = AsyncMock()
    bot.send_message = AsyncMock()
    return bot


@pytest.mark.asyncio
async def test_handle_create_event(mock_consumer, mock_bot):
    """Тест обработки события создания книги"""
    # Подготавливаем тестовые данные
    test_data = {
        "event_type": "create",
        "payload": {"title": "Test Book", "author": "Test Author", "year": 2024},
    }

    # Настраиваем мок консьюмера
    mock_consumer.__aiter__.return_value = [MagicMock(value=orjson.dumps(test_data))]

    # Заменяем реальные объекты на моки
    with (
        patch("bot.bot.AIOKafkaConsumer", return_value=mock_consumer),
        patch("bot.bot.bot", mock_bot),
    ):
        # Запускаем обработку
        await wait_and_send_notifications()

        # Проверяем, что сообщение было отправлено
        mock_bot.send_message.assert_called_once()
        call_args = mock_bot.send_message.call_args[1]
        assert "Была создана книга" in call_args["text"]
        assert "Test Book" in call_args["text"]


@pytest.mark.asyncio
async def test_handle_delete_event(mock_consumer, mock_bot):
    """Тест обработки события удаления книги"""
    test_data = {"event_type": "delete", "payload": {"book_id": 123}}

    mock_consumer.__aiter__.return_value = [MagicMock(value=orjson.dumps(test_data))]

    with (
        patch("bot.bot.AIOKafkaConsumer", return_value=mock_consumer),
        patch("bot.bot.bot", mock_bot),
    ):
        await wait_and_send_notifications()

        mock_bot.send_message.assert_called_once()
        call_args = mock_bot.send_message.call_args[1]
        assert "Была удалена книга с id = 123" in call_args["text"]


@pytest.mark.asyncio
async def test_handle_update_event(mock_consumer, mock_bot):
    """Тест обработки события обновления книги"""
    test_data = {
        "event_type": "update",
        "payload": {"book_id": 123, "title": "Updated Book", "author": "Updated Author"},
    }

    mock_consumer.__aiter__.return_value = [MagicMock(value=orjson.dumps(test_data))]

    with (
        patch("bot.bot.AIOKafkaConsumer", return_value=mock_consumer),
        patch("bot.bot.bot", mock_bot),
    ):
        await wait_and_send_notifications()

        mock_bot.send_message.assert_called_once()
        call_args = mock_bot.send_message.call_args[1]
        assert "Была обновлена книга с id = 123" in call_args["text"]


@pytest.mark.asyncio
async def test_handle_invalid_json(mock_consumer, mock_bot):
    """Тест обработки некорректного JSON"""
    mock_consumer.__aiter__.return_value = [MagicMock(value=b"invalid json")]

    with (
        patch("bot.bot.AIOKafkaConsumer", return_value=mock_consumer),
        patch("bot.bot.bot", mock_bot),
    ):
        await wait_and_send_notifications()

        # Проверяем, что сообщение не было отправлено
        mock_bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_handle_unknown_event_type(mock_consumer, mock_bot):
    """Тест обработки неизвестного типа события"""
    test_data = {"event_type": "unknown", "payload": {}}

    mock_consumer.__aiter__.return_value = [MagicMock(value=orjson.dumps(test_data))]

    with (
        patch("bot.bot.AIOKafkaConsumer", return_value=mock_consumer),
        patch("bot.bot.bot", mock_bot),
    ):
        await wait_and_send_notifications()

        # Проверяем, что сообщение не было отправлено
        mock_bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_config_validation():
    """Тест валидации конфигурации"""
    # Сохраняем оригинальные переменные окружения
    original_env = dict(os.environ)

    try:
        # Очищаем переменные окружения
        os.environ.clear()
        os.environ["BOT_TOKEN"] = ""

        # Удаляем модуль из sys.modules, чтобы он был перезагружен
        if "bot.bot" in sys.modules:
            del sys.modules["bot.bot"]

        # Импортируем модуль заново
        with pytest.raises(ValueError, match="BOT_TOKEN is not set"):
            import bot.bot  # noqa
    finally:
        # Восстанавливаем оригинальные переменные окружения
        os.environ.clear()
        os.environ.update(original_env)
