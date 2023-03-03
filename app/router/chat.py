from collections.abc import Callable

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import UserModel
from app.model.schema.open_ai import ChatGPTMessage, Role
from app.util.query.message import save_message, get_last_one_hundred_messages_by_user
from app.util.query.user import get_user_by_telegram_id, save_user_to_database

chat_router = Router(name="start router")


@chat_router.message(Command("start", "help"))
async def command_start_handler(
    message: Message,
    async_session: AsyncSession,
    telegram_user: TelegramUser,
) -> None:
    user: UserModel | None = await get_user_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_user.id,
    )

    if not user:
        await save_user_to_database(
            async_session=async_session,
            telegram_user=telegram_user,
        )

        await message.reply(
            text=f"Welcome, {telegram_user.full_name}!",
            parse_mode="HTML",
        )
        return

    await message.reply(text=f"Hello, {telegram_user.full_name}!")


@chat_router.message()
async def text_handler(
    message: Message,
    async_session: AsyncSession,
    chat_prompt: Callable[[list[ChatGPTMessage]], ChatGPTMessage],
    telegram_user: TelegramUser,
    message_text: str,
) -> None:
    user: UserModel | None = await get_user_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_user.id,
    )

    if not user:
        raise ValueError("User not found")

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

    answer = chat_prompt([*previous_messages, user_prompt])

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

    await message.reply(text=answer.content)
