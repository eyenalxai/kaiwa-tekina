from collections.abc import Sequence

from aiogram.types import User as TelegramUser
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.model.models import MessageModel, UserModel


async def get_user_by_telegram_id(
    async_session: AsyncSession,
    telegram_id: int,
) -> UserModel | None:
    result = await async_session.execute(
        select(UserModel).where(UserModel.telegram_id == telegram_id),
    )

    return result.scalars().first()


async def save_or_update_user(
    async_session: AsyncSession,
    telegram_user: TelegramUser,
) -> UserModel:
    query = select(UserModel).where(UserModel.telegram_id == telegram_user.id)

    user_result = await async_session.execute(query)

    user: UserModel | None = user_result.scalars().first()

    if not user:
        user = UserModel(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            full_name=telegram_user.full_name,
            is_allowed=False,
        )
        async_session.add(user)
        return user

    user.username = telegram_user.username
    user.full_name = telegram_user.full_name

    return user


async def toggle_allowed_user_by_telegram_id(
    async_session: AsyncSession,
    telegram_id: int,
) -> UserModel:
    user = await get_user_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_id,
    )

    if not user:
        user = UserModel(
            telegram_id=telegram_id,
            is_allowed=True,
        )
        async_session.add(user)
        return user

    user.is_allowed = not user.is_allowed
    return user


async def get_users_with_most_tokens_used(
    async_session: AsyncSession,
    limit: int,
) -> Sequence[tuple[UserModel, int]]:
    query = (
        select(UserModel, func.sum(MessageModel.tokens_used).label("total_tokens_used"))
        .join(MessageModel, UserModel.id == MessageModel.user_id)
        .group_by(UserModel.id)
        .order_by(func.sum(MessageModel.tokens_used).desc())
        .limit(limit)
        .options(
            selectinload(UserModel.messages),
        )
    )

    result = await async_session.execute(query)

    return result.all()  # type: ignore
