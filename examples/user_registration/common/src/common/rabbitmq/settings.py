from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RMQ_",
        extra="ignore",
    )

    url: str
