from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import MessageModel, UserModel
from app.model.schema.open_ai import ChatGPTMessage
from app.util.settings import shared_settings


async def save_message(
    async_session: AsyncSession,
    chat_gpt_message: ChatGPTMessage,
    user: UserModel,
) -> None:
    message = MessageModel(
        role=chat_gpt_message.role,
        content=chat_gpt_message.content,
        user=user,
    )

    async_session.add(message)


async def get_last_messages_by_user(
    async_session: AsyncSession,
    user: UserModel,
) -> Sequence[MessageModel]:
    query = (
        select(MessageModel)
        .where(MessageModel.user == user)
        .order_by(MessageModel.created_at.desc())
        .limit(shared_settings.messages_limit)
    )

    result = await async_session.execute(query)

    return result.scalars().all()
