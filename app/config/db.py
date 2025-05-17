from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@event-db:5432/event_db"


db_settings = DatabaseConfig()
