from typing import Literal

from pydantic import BaseSettings, Field, validator


class SharedSettings(BaseSettings):
    telegram_token: str = Field(..., env="TELEGRAM_TOKEN")

    poll_type: Literal["WEBHOOK", "POLLING"] = Field(..., env="POLL_TYPE")
    port: int = Field(..., env="PORT")
    domain: str = Field(..., env="DOMAIN")
    host: str = Field(env="HOST", default="0.0.0.0")
    main_bot_path: str = "/webhook/main"

    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size = 20

    openai_token: str = Field(..., env="OPENAI_TOKEN")
    openai_chat_api_url = "https://api.openai.com/v1/chat/completions"

    @property
    def async_database_url(self: "SharedSettings") -> str:
        return self.database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
        )

    @property
    def webhook_url(self: "SharedSettings") -> str:
        return "https://{domain}{main_bot_path}".format(
            domain=self.domain,
            main_bot_path=self.main_bot_path,
        )

    # N805 first argument of a method should be named 'self'
    @validator("database_url")
    def validate_database_url(
        cls: "SharedSettings",  # noqa: N805
        v: str,  # noqa: WPS111 Found too short name
    ) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with postgresql://")
        return v


shared_settings = SharedSettings()
