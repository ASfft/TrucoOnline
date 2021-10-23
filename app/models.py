from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, ARRAY, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Game(Base):

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_finished = Column(Boolean, default=False)
    is_full = Column(Boolean, default=False)
    players: List["GamePlayer"] = relationship("GamePlayer", back_populates="game", cascade="delete, delete-orphan")

    def as_json(self):
        return {
            "id": self.id,
            "players": [player.player_id for player in self.players],
            "is_finished": self.is_finished,
            "is_full": self.is_full,
        }


class GamePlayer(Base):

    __tablename__ = "game_players"

    player_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)

    game = relationship("Game")


class Truco(Base):

    __tablename__ = "truco"

    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    all_cards = Column(ARRAY(String), default=[])
    play_cards = Column(JSON, default={})

    player1_points = Column(Integer, default=0)
    player1_cards = Column(ARRAY(String), default=[])
    player1_round_points = Column(Integer, default=0)

    player2_points = Column(Integer, default=0)
    player2_cards = Column(ARRAY(String), default=[])
    player2_round_points = Column(Integer, default=0)

    def as_json(self):
        return {
            "game_id": self.game_id,
            "all_cards": self.all_cards,
            "play_cards": self.play_cards,
            "player1_points": self.player1_points,
            "player1_cards": self.player1_cards,
            "player1_round_points": self.player1_round_points,
            "player2_points": self.player2_points,
            "player2_cards": self.player2_cards,
            "player2_round_points": self.player2_round_points
        }


