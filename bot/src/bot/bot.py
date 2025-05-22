import asyncio
import logging

import environ
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@environ.config(prefix="backend", frozen=True)
class EndpointConfig:
    host: str = environ.var(default="localhost")
    port: int = environ.var(default=8000)

    @property
    def endpoint(self) -> str:
        return f"http://{self.host}:{self.port}"


@environ.config(frozen=True, prefix="BOT")
class Config:
    token: str = environ.var(default="")
    backend: EndpointConfig = environ.group(EndpointConfig)


logger.info("\n" + environ.generate_help(Config))
config: Config = Config.from_environ()

if config.token == "":
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(token=config.token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я твой бот. Используй /help для списка команд."
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
    Список доступных команд:
    /start - Начать взаимодействие с ботом
    /help - Показать это сообщение
    """
    await message.answer(help_text)


@dp.message(F.text)
async def handle_text(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")


def run():
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    run()
