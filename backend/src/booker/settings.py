import environ

PREFIX = "PROJECT"


@environ.config(frozen=True)
class PostgresConfig:
    database: str = environ.var()
    user: str = environ.var()
    password: str = environ.var()
    host: str = environ.var()
    port: int = environ.var()

    @property
    def endpoint(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@environ.config(frozen=True)
class EmbedderConfig:
    host: str = environ.var()
    port: int = environ.var()

    @property
    def endpoint(self) -> str:
        return f"http://{self.host}:{self.port}"


@environ.config(frozen=True)
class CommonConfig:
    version: str = environ.var(default="0.1.0")


@environ.config(prefix=PREFIX, frozen=True)
class WebServerConfig:
    postgres: PostgresConfig = environ.group(
        PostgresConfig,
    )
    common: CommonConfig = environ.group(
        CommonConfig,
    )
    embedder: EmbedderConfig = environ.group(EmbedderConfig)
