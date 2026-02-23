from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  
    )

    APP_HOST: str = Field(default="http://localhost:8000", description="Хост приложения")

    MAX_CODE_GENERATION_ATTEMPTS: int = Field(default=10, ge=1, le=100)
    CODE_LENGTH: int = Field(default=10, ge=4, le=20)

    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_HOST: str = Field(default="postgres")
    DB_PORT: int = Field(default=5432, ge=1, le=65535)  # Исправлено: было DB_HOST
    DB_NAME: str = Field(default="shortener_db")

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    REDIS_HOST: str = Field(default="redis")
    REDIS_PORT: int = Field(default=6379, ge=1, le=65535)
    REDIS_DB: int = Field(default=0, ge=0, le=15)
    REDIS_PASSWORD: str | None = Field(default=None)

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}"
                f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            )
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()