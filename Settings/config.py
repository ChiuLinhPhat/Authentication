import secrets
import warnings
from typing import Annotated, Any, Literal, Optional

from pydantic import (
    AnyUrl,
    HttpUrl,
    MySQLDsn, BeforeValidator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import SettingsConfigDict,BaseSettings
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    PROJECT_NAME: str ="Authentication"
    SENTRY_DSN: Optional[HttpUrl] = None
    SQL_SERVER: str = "127.0.0.1"
    SQL_PORT: int = 3306
    SQL_USER: str = "root"
    SQL_PASSWORD: str =""
    SQL_DB: str = "blog"
    CORS_ORIGINS: list[str] | None = None
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] | None = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        # Constructing the database URI using the provided configuration
        return MultiHostUrl.build(
            scheme="mysql+mysqldb",
            username=self.SQL_USER,
            password=self.SQL_PASSWORD,
            host=self.SQL_SERVER,
            port=self.SQL_PORT,
            path=self.SQL_DB,
        )


DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


settings = Settings()