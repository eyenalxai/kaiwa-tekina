import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config.log import logger
from app.task.prune_messages import prune_messages_task


def main() -> None:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        func=prune_messages_task,
        trigger="cron",
        minute="*/5",
        hour="*",
        day="*",
    )

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping scheduler")
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
