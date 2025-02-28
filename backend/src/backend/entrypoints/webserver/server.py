from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig

from backend.entrypoints.webserver.controllers.version import get_version
from backend.settings import WebServerConfig


def create_server(config: WebServerConfig) -> Litestar:
    # Настройка CORS
    cors_config = CORSConfig(
        allow_origins=["*"],  # В продакшене следует ограничить
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Настройка OpenAPI документации
    openapi_config = OpenAPIConfig(
        title="API Documentation",
        version=config.common.version,
        description="API для проекта DevOps-Spring-2025",
    )

    app = Litestar(
        route_handlers=[get_version],
        dependencies={"config": lambda: config},
        cors_config=cors_config,
        openapi_config=openapi_config,
        debug=True,
    )

    return app
