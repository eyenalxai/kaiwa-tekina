from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession
from tiktoken import Encoding

from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage
from app.model.schema.user import User
from app.util.messages import get_previous_messages
from app.util.open_ai.chat_gpt import token_reducer


def parse_telegram_id(message_text: str) -> int:
    parts = message_text.split()

    if len(parts) != 2:
        raise ValueError("Invalid message text provided")

    return int(parts[1])


def username_or_full_name(user: User) -> str:
    if user.username:
        return "@{username}".format(username=user.username)

    if user.full_name:
        return "{full_name}".format(full_name=user.full_name)

    return str(user.telegram_id)


def split_text(text: str) -> list[str]:
    telegram_limit = 4096
    return [
        text[idx : idx + telegram_limit]  # noqa: E203 whitespace before ':'
        for idx in range(0, len(text), telegram_limit)
    ]


async def get_previous_messages_with_token_adjusted(
    async_session: AsyncSession,
    fernet: Fernet,
    tokenizer: Encoding,
    user: UserModel,
) -> list[ChatGPTMessage]:
    previous_messages = await get_previous_messages(
        async_session=async_session,
        fernet=fernet,
        user=user,
    )

    return token_reducer(
        previous_messages=previous_messages,
        tokenizer=tokenizer,
    )
