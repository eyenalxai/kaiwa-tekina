from aiogram import Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation

from app.middleware.access import filter_non_allowed
from app.middleware.admin import filter_non_admin
from app.router.chat import chat_router
from app.router.management import management_router
from app.router.start import start_router
from app.util.dispatcher.add_stuff import add_message_middleware, add_routes, add_stuff
from app.util.lifecycle.lifecycle_functions import on_shutdown, on_startup


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())
    dispatcher = add_stuff(dispatcher=dispatcher)
    dispatcher = add_routes(dispatcher=dispatcher)

    dispatcher = add_message_middleware(dispatcher=dispatcher)
    management_router.message.middleware(filter_non_admin)

    start_router.message.middleware(filter_non_allowed)
    chat_router.message.middleware(filter_non_allowed)

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    return dispatcher
