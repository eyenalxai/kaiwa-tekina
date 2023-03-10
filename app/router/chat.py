from collections.abc import Callable

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession
from tiktoken import Encoding

from app.config.log import logger
from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage, OpenAIError
from app.util.messages import save_messages
from app.util.open_ai.chat_gpt import ReturnType, respond_to_chat_message
from app.util.stuff import split_text

chat_router = Router(name="chat router")


@chat_router.message()
async def text_handler(  # noqa: WPS211 Found too many arguments
    message: Message,
    async_session: AsyncSession,
    fernet: Fernet,
    tokenizer: Encoding,
    user: UserModel,
    chat_prompt: Callable[[list[ChatGPTMessage]], tuple[int, ReturnType]],
    message_text: str,
) -> None:
    tokens_used, answer = await respond_to_chat_message(
        async_session=async_session,
        fernet=fernet,
        tokenizer=tokenizer,
        user=user,
        chat_prompt=chat_prompt,
        message_text=message_text,
    )

    if isinstance(answer, OpenAIError):
        await message.reply(
            text="\n\n".join(
                [
                    "Can't send you a reply, please try asking in a different way",
                    "Here is an error that I got:\n<i>{error_message}</i>".format(
                        error_message=answer.error.message,
                    ),
                ],
            ),
        )
        return

    await save_messages(
        async_session=async_session,
        message_text=message_text,
        user=user,
        fernet=fernet,
        answer=answer,
        tokens_used=tokens_used,
    )

    parts = split_text(text=answer.content)

    try:
        for part in parts:
            await message.answer(text=part)
    except TelegramBadRequest as exception:
        logger.error(exception.message)
        await message.reply(
            text="\n\n".join(
                [
                    "Can't send you a reply, please try asking in a different way",
                    "Here is an error that I got:\n<i>{error_message}</i>".format(
                        error_message=exception.message,
                    ),
                ],
            ),
        )
