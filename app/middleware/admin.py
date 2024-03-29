from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject
from aiogram.types import User as TelegramUser

from app.util.settings.bot import BotSettings


async def filter_non_admin(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    telegram_user: TelegramUser = data["telegram_user"]

    bot_settings: BotSettings = data["bot_settings"]

    if telegram_user.id not in bot_settings.admin_user_ids:
        return await message.answer("You are not allowed")

    return await handler(message, data)
