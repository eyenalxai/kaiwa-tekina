from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_database_session(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    async with AsyncSession(bind=data["async_engine"]) as async_session:
        async with async_session.begin():
            data["async_session"] = async_session
            return await handler(message, data)
