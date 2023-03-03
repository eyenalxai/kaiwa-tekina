from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import UserModel
from app.util.money import tokens_to_usd
from app.util.query.user import (
    toggle_allowed_user_by_telegram_id,
    get_users_with_most_tokens_used,
)
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


def username_or_full_name(user: UserModel) -> str:
    if user.username:
        return "@{username}".format(username=user.username)

    if user.full_name:
        return "{full_name}".format(full_name=user.full_name)

    return str(user.telegram_id)


@management_router.message(Command("list"))
async def command_list_handler(
    message: Message,
    async_session: AsyncSession,
) -> None:
    users = await get_users_with_most_tokens_used(
        async_session=async_session,
        limit=10,
    )

    users_list = "\n".join(
        "{username}: ${money}".format(
            username=username_or_full_name(user),
            money=tokens_to_usd(tokens=user.tokens_used),
        )
        for user in users
        if tokens_to_usd(tokens=user.tokens_used) > 0
    )

    if not users_list:
        await message.reply(
            text="No users found that spent more than $0",
        )
        return

    message_text = "Top 10 users by tokens used:\n\n{users_list}".format(
        users_list=users_list,
    )

    await message.reply(text=message_text)
