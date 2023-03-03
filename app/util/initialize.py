from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine

from app.middleware.database_session import get_async_database_session
from app.middleware.text import filter_non_text
from app.middleware.user import filter_non_user
from app.router.chat import chat_router
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

    dispatcher.include_router(chat_router)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    dispatcher.message.middleware(filter_non_user)
    dispatcher.message.middleware(filter_non_text)
    dispatcher.message.middleware(get_async_database_session)

    return dispatcher
