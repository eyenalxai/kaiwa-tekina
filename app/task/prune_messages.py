from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.log import logger
from app.model.models import UserModel
from app.model.schema.user import User
from app.util.query.message import delete_messages_for_user_older_than_days
from app.util.query.user import get_all_allowed_users
from app.util.settings.shared import shared_settings
from app.util.settings.worker import worker_settings
from app.util.stuff import username_or_full_name


async def prune_message(
    async_session: AsyncSession,
    user_model: UserModel,
    prune_older_than_days: int,
) -> None:
    deleted_count = await delete_messages_for_user_older_than_days(
        async_session=async_session,
        user=user_model,
        older_than_days=prune_older_than_days,
    )

    if deleted_count > 0:
        user = User(
            username=user_model.username,
            full_name=user_model.full_name,
            telegram_id=user_model.telegram_id,
        )

        identifier = username_or_full_name(user=user)

        message: str = "Deleted {deleted} messages for user {identifier}".format(
            deleted=deleted_count,
            identifier=identifier,
        )

        logger.info(message)


async def prune_messages_task() -> None:
    async_engine = create_async_engine(
        url=shared_settings.async_database_url,
        pool_size=shared_settings.database_pool_size,
        pool_pre_ping=True,
    )

    async with AsyncSession(bind=async_engine) as async_session:
        async with async_session.begin():
            allowed_users = await get_all_allowed_users(async_session=async_session)

            for user in allowed_users:
                await prune_message(
                    async_session=async_session,
                    user_model=user,
                    prune_older_than_days=worker_settings.prune_older_than,
                )


if __name__ == "__main__":
    import asyncio  # noqa: WPS433 Found nested import

    asyncio.run(prune_messages_task())
