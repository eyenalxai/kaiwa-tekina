from aiogram import Bot

from app.util.dispatcher.initialize import initialize_dispatcher
from app.util.lifecycle.start import start_bot
from app.util.settings.bot import bot_settings


def main() -> None:
    bot = Bot(bot_settings.telegram_token, parse_mode="HTML")
    dispatcher = initialize_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
