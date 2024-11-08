from functools import lru_cache

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_username}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_app_config() -> AppConfig:
    return AppConfig()
