from pydantic import BaseModel
from sqlalchemy import select

from app.context import RequestContext
from app.exceptions import BadRequest
from app.models import Truco


async def get_truco(context: RequestContext, game_id: int) -> Truco:
    query = select(Truco).where(Truco.game_id == game_id)
    truco = (await context.db_session.execute(query)).scalars().first()
    return truco


class StartRoundSchema(BaseModel):
    game_id: int


class PlayCardSchema(BaseModel):
    game_id: int
    player: str
    card: str
