from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine
from tiktoken import encoding_for_model

from app.middleware.database_session import get_async_database_session
from app.middleware.text import filter_non_text
from app.middleware.user import filter_non_user, update_user
from app.router.chat import chat_router
from app.router.management import management_router
from app.router.start import start_router
from app.util.crypto.initialize import initialize_fernet
from app.util.open_ai.chat_gpt import chat_gpt_wrapper
from app.util.settings import shared_settings


def add_routes(dispatcher: Dispatcher) -> Dispatcher:
    dispatcher.include_router(management_router)
    dispatcher.include_router(start_router)
    dispatcher.include_router(chat_router)

    return dispatcher


def add_message_middleware(dispatcher: Dispatcher) -> Dispatcher:
    dispatcher.message.middleware(filter_non_user)
    dispatcher.message.middleware(filter_non_text)
    dispatcher.message.middleware(get_async_database_session)
    dispatcher.message.middleware(update_user)

    return dispatcher


def add_stuff(dispatcher: Dispatcher) -> Dispatcher:
    dispatcher["async_engine"] = create_async_engine(
        url=shared_settings.async_database_url,
        pool_size=shared_settings.database_pool_size,
        pool_pre_ping=True,
    )

    dispatcher["chat_prompt"] = chat_gpt_wrapper()
    dispatcher["fernet"] = initialize_fernet(key=shared_settings.fernet_key_bytes)
    dispatcher["tokenizer"] = encoding_for_model("gpt-3.5-turbo")

    return dispatcher
