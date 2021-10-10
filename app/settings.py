import asyncio
from functools import cached_property, lru_cache
from pathlib import Path
from typing import List, Callable, Awaitable

from pydantic import BaseSettings, PrivateAttr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Settings(BaseSettings):
    debug_mode: bool = False

    # PostgreSQL
    pg_user: str = "postgres"
    pg_password: str = "test"
    pg_db: str = "postgres"
    pg_port: int = 5435
    pg_host: str = "127.0.0.1"

    _close_tasks: List[Callable[[], Awaitable]] = PrivateAttr(default_factory=list)

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        keep_untouched = (cached_property,)

    @cached_property
    def db_engine(self):
        return create_async_engine(
            f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}",
            echo=False, future=True
        )

    async def create_db_session(self):
        return AsyncSession(self.db_engine, expire_on_commit=False)

    async def close(self):
        await asyncio.gather(*(x() for x in self._close_tasks))
        self._close_tasks.clear()


@lru_cache(maxsize=1)
def get_settings():
    return Settings()  # pragma: no cover
