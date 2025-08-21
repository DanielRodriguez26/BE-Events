from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_host: str = "localhost"
    database_port: str = "5432"
    database_name: str = "events_db"
    database_user: str = "postgres"
    database_password: str = "1234"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application
    debug: bool = True
    api_v1_str: str = "/api/v1"
    project_name: str = "Events API"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
