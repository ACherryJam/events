from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="EMAIL_",
        extra="ignore"
    )

    smtp_server_url: str
    sender_address: str
