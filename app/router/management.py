from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.util.query.user import toggle_allowed_user_by_telegram_id
from app.util.stuff import parse_telegram_id

management_router = Router(name="management router")


@management_router.message(Command("toggle"))
async def command_toggle_handler(
    message: Message,
    async_session: AsyncSession,
    message_text: str,
) -> None:
    try:
        telegram_id = parse_telegram_id(message_text=message_text)
    except ValueError:
        await message.reply(
            text="Invalid telegram id provided\n\nExample: /toggle 123456789",
        )
        return

    user = await toggle_allowed_user_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_id,
    )

    allowed_state = "Allowed" if user.is_allowed else "Disallowed"

    await message.reply(
        text="{allowed_state} user with id: {telegram_id}".format(
            telegram_id=user.telegram_id,
            allowed_state=allowed_state,
        ),
    )
