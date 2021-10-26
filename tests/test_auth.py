from sqlalchemy import select

from app.databases.database import Database
from app.models import User
from tests.client import Client
from tests.utils import create_random_user, create_login_session


async def test_auth_login__expects_failed(anon_user: Client):
    response = await anon_user.post(
        "/auth/login", json={"username": "test", "password": "test"}
    )
    assert response.status_code == 400


async def test_auth_login__expects_successful(anon_user: Client, db: Database):
    username = "THIAGAO BOLADO"
    password = "test123456"
    user = await create_random_user(db, name=username, password=password)
    await db.commit()
    response = await anon_user.post(
        "/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    await db.session.refresh(user)
    data = response.json()
    assert data["user"]["id"] == user.id
    assert data["user"]["name"] == user.name


async def test_auth_login__expects_failed_because_of_password(
    anon_user: Client, db: Database
):
    username = "renan boladao"
    password = "test123456"
    user = await create_random_user(db, name=username, password=password)
    await db.commit()
    response = await anon_user.post(
        "/auth/login", json={"username": username, "password": password + "1"}
    )
    assert response.status_code == 400
    assert response.json()["msg"] == "Dados inválidos"


async def test_register__expects_successful(anon_user: Client, db: Database):
    username = "renan boladao"
    password = "test123456"
    response = await anon_user.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"user": {"id": 1, "name": "renan boladao"}}

    query = select(User).where(User.name == username)
    user = (await db.session.execute(query)).scalars().first()
    assert user.as_json() == {"id": 1, "name": username}


async def test_register__expects_name_already_been_used(
    anon_user: Client, db: Database
):
    username = "renan boladao"
    password = "test123456"
    user = await create_random_user(db, name=username, password=password)
    await db.commit()

    response = await anon_user.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert response.status_code == 400


async def test_anon_register__expects_successful(anon_user: Client, db: Database):
    response = await anon_user.get("/auth/anon")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == 1

    query = select(User).where(User.id == response.json()["user"]["id"])
    user = (await db.session.execute(query)).scalars().first()
    assert user is not None
