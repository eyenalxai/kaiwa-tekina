from collections.abc import Callable

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import logger
from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage, Role
from app.util.query.message import get_last_messages_by_user, save_message

chat_router = Router(name="chat router")


@chat_router.message()
async def text_handler(  # noqa: WPS211 Found too many arguments
    message: Message,
    async_session: AsyncSession,
    fernet: Fernet,
    user: UserModel,
    chat_prompt: Callable[[list[ChatGPTMessage]], tuple[int, ChatGPTMessage]],
    message_text: str,
) -> None:
    previous_messages_models = await get_last_messages_by_user(
        async_session=async_session,
        user=user,
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

    user_prompt = ChatGPTMessage(
        role=Role.USER,
        content=message_text,
    )

    tokens_used, answer = chat_prompt([*previous_messages, user_prompt])

    await save_message(
        async_session=async_session,
        role=Role.USER,
        content=fernet.encrypt(message_text.encode()),
        user=user,
    )

    await save_message(
        async_session=async_session,
        role=Role.ASSISTANT,
        content=fernet.encrypt(answer.content.strip().encode()),
        user=user,
    )

    user.tokens_used += tokens_used

    await async_session.commit()
    try:
        await message.reply(text=answer.content)
    except TelegramBadRequest as e:
        logger.error(e.message)
        reply_error_text = (
            "Can't send you a reply from ChatGPT, please try asking in a different way"
            "\n\nHere is an error that I got:\n<i>{error_message}</i>".format(
                error_message=e.message,
            )
        )
        await message.reply(text=reply_error_text)
