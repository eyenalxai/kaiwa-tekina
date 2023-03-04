from collections.abc import Callable

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import logger
from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage, Role
from app.util.messages import get_previous_messages, save_messages

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
    previous_messages = await get_previous_messages(
        async_session=async_session,
        fernet=fernet,
        user=user,
    )

    tokens_used, answer = chat_prompt(
        [
            *previous_messages,
            ChatGPTMessage(
                role=Role.USER,
                content=message_text,
            ),
        ],
    )

    await save_messages(
        async_session=async_session,
        message_text=message_text,
        user=user,
        fernet=fernet,
        answer=answer,
        tokens_used=tokens_used,
    )

    await async_session.commit()

    parts = [
        answer.content[i : i + 4096]  # noqa: E203
        for i in range(0, len(answer.content), 4096)
    ]

    try:
        for part in parts:
            await message.answer(text=part)
    except TelegramBadRequest as exception:
        logger.error(exception.message)
        reply_error_text = "\n\n".join(
            [
                "Can't send you a reply, please try asking in a different way",
                "Here is an error that I got:\n<i>{error_message}</i>".format(
                    error_message=exception.message,
                ),
            ],
        )
        await message.reply(text=reply_error_text)
