from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject

from app.config.log import logger


async def filter_non_text(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    if not message.text:
        logger.error("No text in message?! Message: {message}".format(message=message))
        return None

    data["message_text"] = message.text

    return await handler(message, data)
