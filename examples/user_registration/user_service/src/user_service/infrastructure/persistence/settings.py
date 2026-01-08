from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLPersistenceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SQL_",
        extra="ignore",
    )

    database_url: str