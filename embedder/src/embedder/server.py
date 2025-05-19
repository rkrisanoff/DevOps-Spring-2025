from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController
import litestar
import click
from sentence_transformers import SentenceTransformer
import uvicorn

model: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")


@litestar.get("/version")
async def get_version() -> dict[str, str]:
    return {"version": "0.4.0"}


@litestar.get("/infer/embedding")
async def get_embeddings(sentences: list[str]) -> list[list[float]]:
    return model.encode(sentences).tolist()


def create_server() -> Litestar:
    cors_config = CORSConfig(
        allow_origins=["*"],
        allow_methods=[
            "GET",
        ],
        allow_headers=["*"],
    )

    openapi_config = OpenAPIConfig(
        title="API Documentation",
        version="0.4.0",
        description="API сервиса embedder DevOps-Spring-2025",
        render_plugins=[litestar.openapi.plugins.ScalarRenderPlugin()],
    )

    root_router = litestar.Router(route_handlers=[get_embeddings], path="/api/v1")

    prometheus_config = PrometheusConfig(group_path=False)

    app = Litestar(
        route_handlers=[get_version, root_router, PrometheusController],
        cors_config=cors_config,
        openapi_config=openapi_config,
        debug=True,
        middleware=[prometheus_config.middleware],
    )

    return app


@click.command()
@click.option("--host", default="0.0.0.0", help="Хост для запуска сервера")
@click.option("--port", default=9999, help="Порт для запуска сервера")
def run(host: str, port: int) -> None:
    app = create_server()

    uvicorn.run(
        app,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    run()
