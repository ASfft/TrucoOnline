from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.exceptions import WrongCredentials
from app.exceptions import BadRequest
from app.models import User


class UsersDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, username: str, password: str) -> User:
        if username and password:
            query = select(User).where(User.name == username.lower())
            user: User = (await self.session.execute(query)).scalars().first()
            if not user:
                raise WrongCredentials()
            if not user.password == password:
                raise WrongCredentials()
            return user
        raise WrongCredentials()

    async def add(self, name: str, password: str):
        query = select(User).where(User.name == name.lower())
        user: User = (await self.session.execute(query)).scalars().first()
        if user:
            raise BadRequest(msg="Usuário já existe.")
        new_user = User()
        new_user.name = name.lower()
        new_user.password = password

        self.session.add(new_user)
        await self.session.flush()

        return new_user
