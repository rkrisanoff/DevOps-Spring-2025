import click
import environ
import uvicorn

from booker.servers.webserver.server import create_server
from booker.settings import WebServerConfig


@click.command()
@click.option("--host", default="0.0.0.0", help="Хост для запуска сервера")
@click.option("--port", default=8000, help="Порт для запуска сервера")
def run_server(host: str, port: int) -> None:
    config = environ.to_config(WebServerConfig)
    app = create_server(config)

    uvicorn.run(
        app,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    run_server()
