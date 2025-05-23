from collections.abc import AsyncGenerator

import litestar
import litestar.openapi
import litestar.openapi.plugins
import orjson
import sqlalchemy
from aiokafka import AIOKafkaProducer
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

from booker.api.rest.controllers.books import BooksController
from booker.api.rest.controllers.version import get_version
from booker.settings import WebServerConfig


def create_server(config: WebServerConfig) -> Litestar:
    async def get_config() -> WebServerConfig:
        return config

    cors_config = CORSConfig(
        allow_origins=["*"],
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    openapi_config = OpenAPIConfig(
        path="/openapi",
        title="API Documentation",
        version=config.common.version,
        description="API для проекта DevOps-Spring-2025",
        render_plugins=[litestar.openapi.plugins.ScalarRenderPlugin()],
    )

    root_router = litestar.Router(route_handlers=[BooksController], path="/api")

    engine = sqlalchemy.ext.asyncio.create_async_engine(
        url=config.postgres.endpoint, pool_pre_ping=True
    )

    async_session_maker = sqlalchemy.ext.asyncio.async_sessionmaker(engine, expire_on_commit=False)

    async def provide_session() -> sqlalchemy.ext.asyncio.AsyncSession:
        async with async_session_maker() as session:
            yield session

    async def provide_producer() -> AsyncGenerator[None, None, AIOKafkaProducer]:
        producer = AIOKafkaProducer(
            bootstrap_servers=config.broker.endpoint,
            value_serializer=orjson.dumps,
            compression_type="gzip",
            # loop=asyncio.get_running_loop(),
        )
        await producer.start()
        yield producer
        await producer.stop()

    prometheus_config = PrometheusConfig(group_path=False)

    app = Litestar(
        route_handlers=[get_version, root_router, PrometheusController],
        dependencies={
            "config": get_config,
            "session": provide_session,
            "producer": provide_producer,
        },
        cors_config=cors_config,
        openapi_config=openapi_config,
        debug=True,
        middleware=[prometheus_config.middleware],
    )

    return app
