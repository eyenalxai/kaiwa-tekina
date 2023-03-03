from app.config.pydantic import Immutable


class User(Immutable):
    class Config:
        orm_mode = True

    username: str | None
    full_name: str | None
    telegram_id: int


class UserUsage(Immutable):
    user: User
    money: float
