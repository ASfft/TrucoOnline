from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.context import RequestContext
from app.models import Game, GamePlayer
from app.databases.exceptions import AlreadyInGame


async def assert_not_in_game(context: RequestContext):
    query = select(GamePlayer).join(Game).\
        where(context.user.id == GamePlayer.player_id, Game.is_finished.is_(False))
    game = (await context.db_session.execute(query)).scalars().first()
    if game:
        raise AlreadyInGame()


async def find_available_games(context: RequestContext):
    query = select(Game).where(Game.is_finished.is_(False), Game.is_full.is_(False))
    game = (await context.db_session.execute(query)).scalars().first()
    return game

