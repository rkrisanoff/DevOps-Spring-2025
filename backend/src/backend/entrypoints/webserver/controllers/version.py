import litestar

from backend.settings import WebServerConfig


@litestar.get("/version")
async def get_version(config: WebServerConfig) -> dict[str, str]:
    return {"version": config.common.version}
