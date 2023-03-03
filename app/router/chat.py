from collections.abc import Callable

from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage, Role
from app.util.query.message import get_last_one_hundred_messages_by_user, save_message

chat_router = Router(name="chat router")


@chat_router.message()
async def text_handler(
    message: Message,
    async_session: AsyncSession,
    user: UserModel,
    chat_prompt: Callable[[list[ChatGPTMessage]], tuple[int, ChatGPTMessage]],
    message_text: str,
) -> None:
    previous_messages_models = await get_last_one_hundred_messages_by_user(
        async_session=async_session,
        user=user,
    )

    previous_messages = [
        ChatGPTMessage(
            role=message.role,
            content=message.content,
        )
        for message in previous_messages_models
    ]

    user_prompt = ChatGPTMessage(
        role=Role.USER,
        content=message_text,
    )

    tokens_used, answer = chat_prompt([*previous_messages, user_prompt])

    await save_message(
        async_session=async_session,
        chat_gpt_message=user_prompt,
        user=user,
    )

    await save_message(
        async_session=async_session,
        chat_gpt_message=answer,
        user=user,
    )

    user.tokens_used += tokens_used

    await message.reply(text=answer.content)
