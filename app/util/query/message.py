from collections.abc import Sequence
from datetime import datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import MessageModel, UserModel
from app.model.schema.open_ai import Role


async def save_message(
    async_session: AsyncSession,
    role: Role,
    content: bytes,
    user: UserModel,
    tokens_used: int | None,
) -> None:
    message = MessageModel(
        role=role,
        content=content,
        user=user,
        tokens_used=tokens_used,
    )

    async_session.add(message)


async def get_last_messages_by_user(
    async_session: AsyncSession,
    user: UserModel,
    messages_limit: int,
) -> Sequence[MessageModel]:
    query = (
        select(MessageModel)
        .where(MessageModel.user == user)
        .order_by(MessageModel.id.desc())
        .limit(messages_limit)
    )

    result = await async_session.execute(query)

    return result.scalars().all()


async def delete_messages_for_user_older_than_days(
    async_session: AsyncSession,
    user: UserModel,
    older_than_days: int,
) -> int:
    query = (
        delete(MessageModel)
        .where(MessageModel.user == user)
        .where(
            MessageModel.created_at < datetime.now() - timedelta(days=older_than_days),
        )
    )

    result = await async_session.execute(query)

    return result.rowcount  # type: ignore
