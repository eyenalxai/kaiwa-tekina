from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import UserModel
from app.model.schema.user import User, UserUsage
from app.util.money import tokens_to_usd
from app.util.query.user import (
    get_users_with_most_tokens_used,
    toggle_allowed_user_by_telegram_id,
)
from app.util.settings.bot import BotSettings
from app.util.stuff import parse_telegram_id, username_or_full_name

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


def create_user_usage(
    *,
    user_model: UserModel,
    tokens_used: int,
    per_token_price: float,
) -> UserUsage:
    return UserUsage(
        user=User(
            telegram_id=user_model.telegram_id,
            username=user_model.username,
            full_name=user_model.full_name,
        ),
        money_spent=tokens_to_usd(
            tokens=tokens_used,
            per_token_price=per_token_price,
        ),
    )


@management_router.message(Command("list"))
async def command_list_handler(  # noqa: WPS210 Found too many local variables
    message: Message,
    async_session: AsyncSession,
    bot_settings: BotSettings,
) -> None:
    user_models = await get_users_with_most_tokens_used(
        async_session=async_session,
        limit=10,
    )

    per_token_price = bot_settings.per_token_price
    users = [
        create_user_usage(
            user_model=user_model,
            tokens_used=tokens_used,
            per_token_price=per_token_price,
        )
        for user_model, tokens_used in user_models
        if tokens_to_usd(tokens=tokens_used, per_token_price=per_token_price) > 0
    ]

    if not users:
        await message.reply(text="No users found that spent more than $0")
        return

    message_text = "Top 10 users by tokens used:\n\n{users_list}".format(
        users_list="\n".join(
            "<code>${money}</code> — {username} ({id})".format(
                id=user_usage.user.telegram_id,
                username=username_or_full_name(user=user_usage.user),
                money=user_usage.money_spent,
            )
            for user_usage in users
        ),
    )

    await message.reply(text=message_text)
