from pydantic import BaseSettings, Field, validator


class SharedSettings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size = 20

    @property
    def async_database_url(self: "SharedSettings") -> str:
        return self.database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
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


shared_settings = SharedSettings()  # type: ignore
