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

    max_tokens_per_request: int = 4096
    per_token_price: float = 0.002

    # Example: [1234567890, 1234567890, ...] # noqa: E800 Found commented out code
    admin_user_ids: list[int] = Field(..., env="ADMIN_USER_IDS")

    messages_limit: int = Field(env="MESSAGES_LIMIT", default=10)

    fernet_key: str = Field(..., env="FERNET_KEY")

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

    @property
    def fernet_key_bytes(self: "SharedSettings") -> bytes:
        return self.fernet_key.encode()

    @property
    def max_prompt_tokens(self: "SharedSettings") -> int:
        return int(
            self.max_tokens_per_request * 0.75,  # noqa: WPS432 Found magic number
        )


shared_settings = SharedSettings()
