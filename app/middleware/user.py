from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import logger
from app.util.query.user import save_or_update_user


async def filter_non_user(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    if not message.from_user:
        logger.error("No user in message?! Message: {message}".format(message=message))
        return None

    data["telegram_user"] = message.from_user

    return await handler(message, data)


async def update_user(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    async_session: AsyncSession = data["async_session"]
    telegram_user: TelegramUser = data["telegram_user"]

    await save_or_update_user(
        async_session=async_session,
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        full_name=telegram_user.full_name,
    )

    return await handler(message, data)
