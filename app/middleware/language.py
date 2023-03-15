from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject
from lingua import LanguageDetector


async def detect_language(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    language_detector: LanguageDetector = data["language_detector"]
    message_text: str = data["message_text"]

    data["language"] = language_detector.detect_language_of(text=message_text)

    return await handler(message, data)
