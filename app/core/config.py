from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    postgres_user: str = "events_user"
    postgres_password: str = "events_password"
    postgres_db: str = "events_db"
    database_host: str = "postgres"  # Default to the service name for Docker
    database_port: str = "5432"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.database_host}:{self.database_port}/{self.postgres_db}"

    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application
    debug: bool = True
    api_v1_str: str = "/api/v1"
    project_name: str = "Events API"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
