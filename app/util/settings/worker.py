from pydantic import BaseSettings, Field


class WorkerSettings(BaseSettings):
    # In days
    prune_older_than: int = Field(..., env="PRUNE_OLDER_THAN_DAYS")


worker_settings = WorkerSettings()  # type: ignore
