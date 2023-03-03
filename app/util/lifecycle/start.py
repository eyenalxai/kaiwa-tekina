from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.util.health_check import health_check_endpoint
from app.util.settings import shared_settings


def start_bot(dispatcher: Dispatcher, bot: Bot) -> None:
    if shared_settings.poll_type == "WEBHOOK":
        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(
            app,
            path=shared_settings.main_bot_path,
        )
        setup_application(app, dispatcher, bot=bot)
        app.add_routes([web.get("/health", health_check_endpoint)])
        web.run_app(app, host=shared_settings.host, port=shared_settings.port)

    if shared_settings.poll_type == "POLLING":
        dispatcher.run_polling(bot, skip_updates=True)
