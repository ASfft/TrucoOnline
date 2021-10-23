from sqlalchemy.ext.asyncio import AsyncSession

from .games import GamesDatabase
from .truco import TrucosDatabase
from .users import UsersDatabase


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UsersDatabase(self.session)
        self.games = GamesDatabase(self.session)
        self.trucos = TrucosDatabase(self.session)

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def refresh(self, *args, **kwargs):
        await self.session.refresh(*args, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
            raise exc_val
        else:
            await self.commit()
