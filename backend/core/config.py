from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote_plus as url_quote
import os
from pydantic import AnyHttpUrl, BaseSettings, validator
import os


class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    APP_VERSION: str

    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: str
    DB_DRIVER: str
    DATABASE_URI: Optional[str] = None

    DB_POOL_SIZE: int
    DB_POOL_MAX_OVERFLOW: int

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return "{DB_DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}".format(
            USER=values.get("DB_USER"),
            PASSWORD=url_quote(values.get("DB_PASS")),
            HOST=values.get("DB_HOST"),
            PORT=values.get("DB_PORT"),
            DATABASE=values.get("DB_NAME"),
            DB_DRIVER=values.get("DB_DRIVER")
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
