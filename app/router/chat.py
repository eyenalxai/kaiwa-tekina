from collections.abc import Callable

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from cryptography.fernet import Fernet
from lingua import Language
from sqlalchemy.ext.asyncio import AsyncSession
from tiktoken import Encoding

from app.config.log import logger
from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage
from app.util.display.html import markdown_to_html
from app.util.open_ai.chat_gpt import respond_to_chat_message
from app.util.open_ai.send_request import OpenAIError
from app.util.placeholder import get_placeholder
from app.util.settings import SharedSettings
from app.util.stuff import split_text_into_parts

chat_router = Router(name="chat router")


async def send_error_message(*, message: Message, error_message: str) -> None:
    await message.reply(
        text="\n\n".join(
            [
                "Can't send you a reply, please try asking in a different way",
                "Here is an error that I got:\n<i>{error_message}</i>".format(
                    error_message=error_message,
                ),
            ],
        ),
    )


# WPS217 Found too many await expressions: 7 > 5
# WPS211 Found too many arguments
@chat_router.message()
async def text_handler(  # noqa: WPS211, WPS217
    message: Message,
    async_session: AsyncSession,
    fernet: Fernet,
    tokenizer: Encoding,
    settings: SharedSettings,
    language: Language | None,
    user: UserModel,
    chat_prompt: Callable[[list[ChatGPTMessage]], tuple[int, ChatGPTMessage]],
    message_text: str,
) -> None:
    sent_message = await message.answer(text=get_placeholder(language=language))

    try:
        answer = await respond_to_chat_message(
            async_session=async_session,
            fernet=fernet,
            tokenizer=tokenizer,
            user=user,
            chat_prompt=chat_prompt,
            message_text=message_text,
            max_prompt_tokens=settings.max_prompt_tokens,
            messages_limit=settings.messages_limit,
        )
    except OpenAIError as open_ai_error:
        return await send_error_message(
            message=message,
            error_message=open_ai_error.message,
        )

    try:
        await sent_message.delete()
        for part in split_text_into_parts(text=answer.content):
            await message.answer(text=markdown_to_html(text=part))
    except TelegramBadRequest as exception:
        logger.error(exception.message)
        return await send_error_message(
            message=message,
            error_message=exception.message,
        )
