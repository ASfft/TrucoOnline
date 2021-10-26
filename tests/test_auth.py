from app.databases.database import Database
from tests.client import Client
from tests.utils import create_random_user, create_login_session


async def test_auth_login__expects_failed(anon_user: Client):
    response = await anon_user.post(
        "/auth/login", json={"username": "test", "password": "test"}
    )
    assert response.status_code == 400


async def test_auth_login__expects_success(anon_user: Client, db: Database):
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


async def test_logout__expects_successful(anon_user: Client, db: Database):
    response, user = await create_login_session(db, anon_user)
    response = await anon_user.post(
        "/auth/logout", cookies={"SESSION_ID": response.cookies["SESSION_ID"]}
    )
    assert response.status_code == 200
    assert len(response.cookies) == 0
