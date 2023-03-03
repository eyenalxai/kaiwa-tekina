from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject

from app.config.log import logger


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
