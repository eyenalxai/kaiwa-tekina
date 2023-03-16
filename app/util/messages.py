from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage, Role
from app.util.query.message import get_last_messages_by_user, save_message


async def get_previous_messages(
    *,
    async_session: AsyncSession,
    fernet: Fernet,
    user: UserModel,
    messages_limit: int,
) -> list[ChatGPTMessage]:
    previous_messages_models = await get_last_messages_by_user(
        async_session=async_session,
        user=user,
        messages_limit=messages_limit,
    )

    previous_messages = reversed(
        [
            ChatGPTMessage(
                role=message.role,
                content=fernet.decrypt(message.content).decode(),
            )
            for message in previous_messages_models
        ],
    )

    return list(previous_messages)


async def save_messages(  # noqa:  WPS211 Found too many arguments: 6 > 5
    *,
    async_session: AsyncSession,
    message_text: str,
    user: UserModel,
    fernet: Fernet,
    answer: ChatGPTMessage,
    tokens_used: int,
) -> None:
    await save_message(
        async_session=async_session,
        role=Role.USER,
        content=fernet.encrypt(message_text.encode()),
        user=user,
        tokens_used=None,
    )

    await save_message(
        async_session=async_session,
        role=Role.ASSISTANT,
        content=fernet.encrypt(answer.content.strip().encode()),
        user=user,
        tokens_used=tokens_used,
    )

    await async_session.commit()
