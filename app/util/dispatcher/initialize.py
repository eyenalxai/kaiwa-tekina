from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine

from app.middleware.access import filter_non_allowed
from app.middleware.admin import filter_non_admin
from app.router.chat import chat_router
from app.router.management import management_router
from app.router.start import start_router
from app.util.crypto.initialize import initialize_fernet
from app.util.dispatcher.oof import add_message_middleware, add_routes
from app.util.lifecycle.lifecycle_functions import on_shutdown, on_startup
from app.util.open_ai.chat_gpt import chat_gpt_wrapper
from app.util.settings import shared_settings


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher["async_engine"] = create_async_engine(
        url=shared_settings.async_database_url,
        pool_size=shared_settings.database_pool_size,
        pool_pre_ping=True,
    )

    dispatcher["chat_prompt"] = chat_gpt_wrapper()
    dispatcher["fernet"] = initialize_fernet(key=shared_settings.fernet_key_bytes)

    dispatcher = add_routes(dispatcher=dispatcher)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    dispatcher = add_message_middleware(dispatcher=dispatcher)
    management_router.message.middleware(filter_non_admin)

    start_router.message.middleware(filter_non_allowed)
    chat_router.message.middleware(filter_non_allowed)

    return dispatcher
