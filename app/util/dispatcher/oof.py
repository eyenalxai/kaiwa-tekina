from aiogram import Dispatcher

from app.middleware.database_session import get_async_database_session
from app.middleware.text import filter_non_text
from app.middleware.user import filter_non_user, update_user
from app.router.chat import chat_router
from app.router.management import management_router
from app.router.start import start_router


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
