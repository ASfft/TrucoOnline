from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.context import RequestContext, get_context
from app.queue.helpers import assert_not_in_game, find_available_games

router = APIRouter()


@router.post("/online")
async def join_queue(context: RequestContext = Depends(get_context)):
    await assert_not_in_game(context)
    game = await find_available_games(context)
    async with context.db as db:
        if game:
            await db.games.update(
                game.id,
                users_id=[context.user.id],
                is_append=True
            )
            await db.session.refresh(game)
        else:
            game = await db.games.add(users_id=[context.user.id])
    data = await db.session.run_sync(lambda x: game.as_json())
    return ORJSONResponse(
        {
            "msg": "Bem sucedido!",
            "status": 200,
            "game": data,
        },
        status_code=200,
    )
