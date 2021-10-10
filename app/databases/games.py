from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.exceptions import GamePlayersLimitExceed
from app.models import Game, GamePlayer


class GamesDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, users_id: List[int]) -> Game:
        new_game = Game()
        if len(users_id) == 2:
            new_game.is_full = True
        self.session.add(new_game)
        await self.session.flush()
        if users_id:
            for player_id in users_id:
                new_game_player = GamePlayer()
                new_game_player.player_id = player_id
                new_game_player.game_id = new_game.id
                self.session.add(new_game_player)
            await self.session.flush()
        return new_game

    async def update(self, game_id: int, users_id: List[int], is_append: bool = False):
        if users_id is not None:
            if not is_append:
                if len(users_id) > 2:
                    raise GamePlayersLimitExceed()
                if len(users_id) == 2:
                    await self.session.execute(
                        update(Game).where(Game.id == game_id).values(is_full=True)
                    )
                await self.session.execute(
                    delete(GamePlayer).where(GamePlayer.game_id == game_id)
                )
                await self.session.flush()
            else:
                n_players = len(
                    (
                        await self.session.execute(
                            select(GamePlayer).where(GamePlayer.game_id == game_id)
                        )
                    )
                    .scalars()
                    .all()
                )
                if n_players + len(users_id) > 2:
                    raise GamePlayersLimitExceed()
                if n_players + len(users_id) == 2:
                    await self.session.execute(
                        update(Game).where(Game.id == game_id).values(is_full=True)
                    )
            for player_id in users_id:
                new_game_player = GamePlayer()
                new_game_player.player_id = player_id
                new_game_player.game_id = game_id
                self.session.add(new_game_player)
            if is_append:
                await self.session.execute(
                    update(Game).where(Game.id == game_id).values(is_full=True)
                )

        await self.session.flush()
