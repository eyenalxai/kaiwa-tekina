from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import User as TelegramUser

start_router = Router(name="start router")


@start_router.message(Command("start", "help"))
async def command_start_handler(
    message: Message,
    telegram_user: TelegramUser,
) -> None:
    await message.reply(
        text="Hello, {telegram_user.full_name}!\n\nAsk me something!".format(
            telegram_user=telegram_user,
        ),
    )
