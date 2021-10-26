from app.databases.database import Database
from tests.client import Client
from tests.utils import create_random_user, create_random_game


async def test_join_queue__expects_create_new_game(user: Client):
    response = await user.post("/queue/", json={"game_mode": "ia"})
    assert response.status_code == 200
    assert response.json() == {"game_id": 1, "msg": "Bem sucedido!", "status": 200}


async def test_join_queue__expects_join_already_created_game(
    user: Client, db: Database
):
    random_user = await create_random_user(db, name="random_user")
    game = await create_random_game(db, users=[random_user], is_full=False)
    await db.session.commit()

    response = await user.post("/queue/", json={"game_mode": "online"})
    assert response.status_code == 200
    assert response.json() == {"game_id": 1, "msg": "Bem sucedido!", "status": 200}


async def test_join_queue__expects_already_in_game(user: Client, db: Database):
    game = await create_random_game(db, users=[user.user])
    await db.session.commit()

    response = await user.post("/queue/", json={"game_mode": "ia"})
    assert response.status_code == 400
    assert response.json() == {
        "game_id": "1",
        "msg": "Já está em um jogo!",
        "status": 400,
    }
