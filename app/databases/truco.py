from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers import filter_empty_keys
from app.models import Truco


class TrucosDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, game_id, player1_cards=None, player2_cards=None) -> Truco:
        new_truco = Truco()
        new_truco.game_id = game_id
        new_truco.player1_cards = player1_cards or []
        new_truco.player2_cards = player2_cards or []
        self.session.add(new_truco)
        await self.session.commit()
        return new_truco

    async def update(
        self,
        game_id,
        round_value=None,
        play_cards=None,
        turn=None,
        player1_cards=None,
        player2_cards=None,
        player1_points=None,
        player2_points=None,
        player1_round_points=None,
        player2_round_points=None,
        player1_game_points=None,
        player2_game_points=None,
    ):
        data = {
            "round_value": round_value,
            "play_cards": play_cards,
            "turn": turn,
            "player1_cards": player1_cards,
            "player2_cards": player2_cards,
            "player1_points": player1_points,
            "player2_points": player2_points,
            "player1_round_points": player1_round_points,
            "player2_round_points": player2_round_points,
            "player1_game_points": player1_game_points,
            "player2_game_points": player2_game_points,
        }
        filter_empty_keys(data)
        await self.session.execute(
            update(Truco).where(Truco.game_id == game_id).values(**data)
        )
        await self.session.flush()

    async def delete(self, game_id: int):
        await self.session.execute(delete(Truco).where(Truco.game_id == game_id))
        await self.session.flush()
