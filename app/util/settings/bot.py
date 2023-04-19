from typing import Literal

from pydantic import BaseSettings, Field


class BotSettings(BaseSettings):
    telegram_token: str = Field(..., env="TELEGRAM_TOKEN")

    poll_type: Literal["WEBHOOK", "POLLING"] = Field(..., env="POLL_TYPE")
    port: int = Field(..., env="PORT")
    domain: str = Field(..., env="DOMAIN")
    host: str = Field(env="HOST", default="0.0.0.0")
    main_bot_path: str = "/webhook/main/kaiwa-tekina"

    openai_token: str = Field(..., env="OPENAI_TOKEN")
    openai_chat_api_url = "https://api.openai.com/v1/chat/completions"

    max_tokens_per_request: int = 4096
    per_token_price: float = 0.002

    # Example: [1234567890, 1234567890, ...] # noqa: E800 Found commented out code
    admin_user_ids: list[int] = Field(..., env="ADMIN_USER_IDS")

    messages_limit: int = Field(env="MESSAGES_LIMIT", default=10)

    fernet_key: str = Field(..., env="FERNET_KEY")

    @property
    def webhook_url(self: "BotSettings") -> str:
        return "{domain}{main_bot_path}".format(
            domain=self.domain,
            main_bot_path=self.main_bot_path,
        )

    @property
    def fernet_key_bytes(self: "BotSettings") -> bytes:
        return self.fernet_key.encode()

    @property
    def max_prompt_tokens(self: "BotSettings") -> int:
        return int(
            self.max_tokens_per_request * 0.8,  # noqa: WPS432 Found magic number
        )


bot_settings = BotSettings()  # type: ignore
