from typing import List

from sqlalchemy import select

from app.databases.database import Database
from app.models import User, Game
from tests.client import Client


async def create_test_client(
    app,
    settings,
    db,
    password: str = "test123456",
    ip_address: str = "127.0.0.1",
):
    new_user = await create_random_user(db, password=password)
    await db.session.commit()
    return Client(
        app=app,
        user=new_user,
        settings=settings,
        password=password,
        ip_address=ip_address,
    )


async def create_random_user(
    db: Database,
    name: str = "test",
    password: str = "test123456",
) -> User:
    user = await db.users.add(
        name=name,
        password=password,
    )

    query = select(User).where(User.id == user.id)
    return (await db.session.execute(query)).scalars().first()


async def create_login_session(
    db: Database,
    anon_user: Client,
    password: str = "test123454656243",
    user: User = None,
):
    if not user:
        user = await create_random_user(db, password=password)
        await db.commit()
    response = await anon_user.post(
        "/auth/login", json={"username": user.name, "password": password}
    )
    assert response.status_code == 200
    return response, user


async def create_random_game(db: Database, users: List[User]) -> Game:
    game = await db.games.add(users_id=[user.id for user in users])

    query = select(Game).where(Game.id == game.id)
    return (await db.session.execute(query)).scalars().first()
