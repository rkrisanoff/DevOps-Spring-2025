import asyncio
import json
import logging

import environ
import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@environ.config(prefix="broker", frozen=True)
class BrokerConfig:
    host: str = environ.var(default="localhost")
    port: int = environ.var(default=9092)

    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.port}"


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
    broker: BrokerConfig = environ.group(BrokerConfig)
    notification_target_chat_id: int = environ.var(default=-4904260504)


# ##############################################################3333

logger.info("\n" + environ.generate_help(Config))
config: Config = Config.from_environ()

if config.token == "":
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(
    token=config.token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN,
    ),
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ##############################################################3333


# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer(
#         f"Привет, {message.from_user.first_name}! Я твой бот. Используй /help для списка команд."
#     )


# @dp.message(Command("help"))
# async def cmd_help(message: types.Message):
#     help_text = """
#     Список доступных команд:
#     /start - Начать взаимодействие с ботом
#     /help - Показать это сообщение
#     """
#     await message.answer(help_text)


# @dp.message(F.text)
# async def handle_text(message: types.Message):
#     await message.answer(f"Вы написали: {message.text}")

TOPIC = "notifications"
GROUP_ID = "group_id"


async def wait_and_send_notifications() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=config.broker.endpoint,
        group_id=GROUP_ID,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        # loop=asyncio.get_running_loop(),
    )
    await consumer.start()
    try:
        async for message in consumer:
            try:
                data = orjson.loads(message.value)

                match data.get("event_type"):
                    case "delete":
                        notification_message = (
                            f"Была удалена книга с id = {data['payload']['book_id']}"
                        )
                    case "create":
                        notification_message = f"""
                        Была создана книга:

```
{json.dumps(data["payload"], indent=4)}
```
                        """
                    case "update":
                        notification_message = f"""
                        Была обновлена книга с id = {data["payload"]["book_id"]}:

```
{json.dumps(data["payload"], indent=4)}
```
                        """
                    case _:
                        logger.warning("It's wrong 'event_type': %s", data.get("event_type"))
                        continue

                await bot.send_message(
                    chat_id=config.notification_target_chat_id, text=notification_message
                )
                await consumer.commit()
                # topic = message.topic
                # partition = message.partition
                # offset = message.offset

            except orjson.JSONDecodeError:
                logger.error("Ошибка парсинга JSON: %s", message.value)

    finally:
        await consumer.stop()
        print("Консьюмер остановлен")


def run():
    asyncio.run(wait_and_send_notifications())


if __name__ == "__main__":
    run()
