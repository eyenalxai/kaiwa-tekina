from aiogram import Bot

from app.config.log import logger
from app.util.settings import shared_settings


async def on_startup(bot: Bot) -> None:
    if shared_settings.poll_type == "WEBHOOK":
        webhook_url = shared_settings.webhook_url
        await bot.set_webhook(webhook_url)
        logger.info("Webhook set to: {webhook_url}".format(webhook_url=webhook_url))


async def on_shutdown() -> None:
    logger.info("Shutting down...")
