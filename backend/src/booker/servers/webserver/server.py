import litestar
import litestar.openapi
import litestar.openapi.plugins
import sqlalchemy
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig

from booker.api.rest.controllers.books import BooksController
from booker.api.rest.controllers.version import get_version
from booker.settings import WebServerConfig


def create_server(config: WebServerConfig) -> Litestar:
    cors_config = CORSConfig(
        allow_origins=["*"],  # В продакшене следует ограничить
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    openapi_config = OpenAPIConfig(
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

    app = Litestar(
        route_handlers=[get_version, root_router],
        dependencies={"config": lambda: config, "session": provide_session},
        cors_config=cors_config,
        openapi_config=openapi_config,
        debug=True,
    )

    return app
