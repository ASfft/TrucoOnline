from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.context import RequestContext, get_context
from app.exceptions import BadRequest
from app.game.helpers import win_checker, deal_cards, default_deck
from app.game.schemas import PlayCardSchema, get_truco, StartRoundSchema

router = APIRouter()


@router.post("/ia/start")
async def start_ia_game(schema: StartRoundSchema, context: RequestContext = Depends(get_context)):
    truco = await get_truco(context, schema.game_id)
    if not truco:
        deck = default_deck
        player1 = await deal_cards(deck)
        player2 = await deal_cards(deck)
        await context.db.trucos.add(schema.game_id, deck, player1, player2)
    else:
        async with context.db as db:
            truco.all_cards = default_deck
            truco.player1_cards = await deal_cards(truco.all_cards)
            player1 = truco.player1_cards
            truco.player2_cards = await deal_cards(truco.all_cards)
            player2 = truco.player2_cards
            truco.player1_round_points = 0
            truco.player2_round_points = 0
            truco.play_cards = {}
            await db.trucos.update(**truco.as_json())
            await db.session.refresh(truco)
    return ORJSONResponse({"player1_cards": player1, "player2_cards": player2}, status_code=200)


@router.post("/ia/play-card")
async def play_card(schema: PlayCardSchema, context: RequestContext = Depends(get_context)):
    truco = await get_truco(context, schema.game_id)
    if not truco:
        raise BadRequest(msg="Missing Entity")

    if schema.player == "player1":
        truco.player1_cards.remove(schema.card)
        player_cards = truco.player1_cards
    else:
        truco.player2_cards.remove(schema.card)
        player_cards = truco.player2_cards
    truco.play_cards[schema.player[-1]] = schema.card

    result = None
    if len(truco.play_cards) == 2:
        result = await win_checker(truco.play_cards["1"], truco.play_cards["2"])
        if schema.player == "player1":
            truco.player1_round_points += 1
        else:
            truco.player2_round_points += 1

    async with context.db as db:
        await db.trucos.update(**truco.as_json())
        await db.session.refresh(truco)
    return ORJSONResponse({"player_cards": player_cards, "result": result}, status_code=200)
