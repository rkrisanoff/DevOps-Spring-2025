import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types

# Устанавливаем тестовые переменные окружения
os.environ["BOT_TOKEN"] = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Правильный формат токена
os.environ["BOT_BACKEND_HOST"] = "backend"
os.environ["BOT_BACKEND_PORT"] = "8000"

# Мокируем создание бота перед импортом модуля
with patch("aiogram.Bot"):
    from bot.bot import cmd_help, cmd_start, handle_text


@pytest.fixture
def message():
    """Фикстура для создания тестового сообщения"""
    message = AsyncMock(spec=types.Message)
    # Создаем вложенные моки для from_user
    from_user = MagicMock()
    from_user.first_name = "TestUser"
    message.from_user = from_user
    message.text = "test message"
    # Настраиваем асинхронный метод answer
    message.answer = AsyncMock()
    return message


@pytest.mark.asyncio
async def test_cmd_start(message):
    """Тест команды /start"""
    await cmd_start(message)
    message.answer.assert_called_once_with(
        "Привет, TestUser! Я твой бот. Используй /help для списка команд."
    )


@pytest.mark.asyncio
async def test_cmd_help(message):
    """Тест команды /help"""
    await cmd_help(message)
    expected_help_text = """
    Список доступных команд:
    /start - Начать взаимодействие с ботом
    /help - Показать это сообщение
    """
    message.answer.assert_called_once_with(expected_help_text)


@pytest.mark.asyncio
async def test_handle_text(message):
    """Тест обработки текстового сообщения"""
    await handle_text(message)
    message.answer.assert_called_once_with("Вы написали: test message")


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
