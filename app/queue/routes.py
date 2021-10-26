from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.context import RequestContext, get_context
from app.queue.helpers import assert_not_in_game, find_available_games
from app.queue.schemas import JoinQueueSchema

router = APIRouter()


@router.post("/")
async def join_queue(
    schema: JoinQueueSchema, context: RequestContext = Depends(get_context)
):
    await assert_not_in_game(context)
    game = None
    if schema.game_mode == "online":
        game = await find_available_games(context)
    async with context.db as db:
        if game:
            await db.games.update(game.id, users_id=[context.user.id], is_append=True)
            await db.session.refresh(game)
        else:
            game = await db.games.add(
                users_id=[context.user.id], is_full=schema.game_mode == "ia"
            )
    data = await db.session.run_sync(lambda x: game.as_json())
    return ORJSONResponse(
        {
            "msg": "Bem sucedido!",
            "status": 200,
            "game_id": game.id,
        },
        status_code=200,
    )
