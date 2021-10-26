from random import randint
from typing import List

from sqlalchemy import select

from app.context import RequestContext
from app.exceptions import BadRequest
from app.models import GamePlayer


async def assert_user_in_game(context: RequestContext, game_id: int):
    query = select(GamePlayer).where(
        GamePlayer.game_id == game_id, GamePlayer.player_id == context.user.id
    )
    game_player = (await context.db_session.execute(query)).scalars().first()
    if not game_player:
        raise BadRequest(msg="Não pertence ao jogo.")


deck_order = {
    "3-O": 9,
    "3-E": 9,
    "3-C": 9,
    "3-P": 9,
    "2-O": 8,
    "2-E": 8,
    "2-C": 8,
    "2-P": 8,
    "A-O": 7,
    "A-E": 11,
    "A-C": 7,
    "A-P": 7,
    "K-O": 6,
    "K-E": 6,
    "K-C": 6,
    "K-P": 6,
    "J-O": 5,
    "J-E": 5,
    "J-C": 5,
    "J-P": 5,
    "Q-O": 4,
    "Q-E": 4,
    "Q-C": 4,
    "Q-P": 4,
    "7-O": 10,
    "7-E": 3,
    "7-C": 12,
    "7-P": 3,
    "6-O": 2,
    "6-E": 2,
    "6-C": 2,
    "6-P": 2,
    "5-O": 1,
    "5-E": 1,
    "5-C": 1,
    "5-P": 1,
    "4-O": 0,
    "4-E": 0,
    "4-C": 0,
    "4-P": 13,
}

default_deck = [
    "3-O",
    "3-E",
    "3-C",
    "3-P",
    "2-O",
    "2-E",
    "2-C",
    "2-P",
    "A-O",
    "A-E",
    "A-C",
    "A-P",
    "K-O",
    "K-E",
    "K-C",
    "K-P",
    "J-O",
    "J-E",
    "J-C",
    "J-P",
    "Q-O",
    "Q-E",
    "Q-C",
    "Q-P",
    "7-O",
    "7-E",
    "7-C",
    "7-P",
    "6-O",
    "6-E",
    "6-C",
    "6-P",
    "5-O",
    "5-E",
    "5-C",
    "5-P",
    "4-O",
    "4-E",
    "4-C",
    "4-P",
]


async def deal_cards(deck: List[str]):
    cards = []
    while len(cards) < 3:
        chosen_card = randint(0, len(deck) - 1)
        cards.append(deck.pop(chosen_card))
    return cards


async def win_checker(card1, card2):
    card1_value = deck_order.get(card1)
    card2_value = deck_order.get(card2)
    if card1_value > card2_value:
        return 1
    if card1_value < card2_value:
        return 2
    return 0
