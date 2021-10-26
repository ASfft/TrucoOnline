from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.context import RequestContext, get_context
from app.exceptions import BadRequest
from app.game.helpers import win_checker, deal_cards, default_deck, assert_user_in_game
from app.game.schemas import PlayCardSchema, get_truco, TrucoSchema

router = APIRouter()


@router.get("/ia/{game_id}/details")
async def game_details(game_id: int, context: RequestContext = Depends(get_context)):
    await assert_user_in_game(context, game_id)
    truco = await get_truco(context, game_id)
    if not truco:
        deck = default_deck
        player1 = await deal_cards(deck)
        player2 = await deal_cards(deck)
        truco = await context.db.trucos.add(game_id, player1, player2)
    return ORJSONResponse(truco.as_json(), status_code=200)


@router.post("/ia/{game_id}/start")
async def start_round(game_id: int, context: RequestContext = Depends(get_context)):
    await assert_user_in_game(context, game_id)
    truco = await get_truco(context, game_id)
    if not truco:
        raise BadRequest(msg="Missing Entity")
    async with context.db as db:
        deck = default_deck[:]
        truco.player1_cards = await deal_cards(deck)
        truco.player2_cards = await deal_cards(deck)
        truco.player1_round_points = 0
        truco.player2_round_points = 0
        truco.round_value = 2
        truco.play_cards = {}
        truco.turn = "player2" if truco.last_round_starter == "player1" else "player1"
        truco.last_round_starter = truco.turn
        await db.trucos.update(**truco.as_json(is_update=True))
        await db.session.refresh(truco)
    return ORJSONResponse(truco.as_json(), status_code=200)


@router.post("/ia/{game_id}/play-card")
async def play_card(
    game_id: int, schema: PlayCardSchema, context: RequestContext = Depends(get_context)
):
    await assert_user_in_game(context, game_id)
    truco = await get_truco(context, game_id)
    if not truco:
        raise BadRequest(msg="Missing Entity")

    if schema.player == "player1":
        truco.player1_cards.remove(schema.card)
        truco.turn = "player2"
    else:
        truco.player2_cards.remove(schema.card)
        truco.turn = "player1"
    truco.play_cards[schema.player[-1]] = schema.card

    play_winner = None
    round_finished = False
    game_finished = False
    game_completed = False
    if len(truco.play_cards) == 2:
        play_winner = await win_checker(truco.play_cards["1"], truco.play_cards["2"])
        first_round = (truco.player1_round_points + truco.player2_round_points) == 0
        if play_winner == 1:
            truco.player1_round_points += 1 if not first_round else 1.25
            truco.turn = "player1"
        elif play_winner == 2:
            truco.player2_round_points += 1 if not first_round else 1.25
            truco.turn = "player2"
        else:
            truco.player1_round_points += 1
            truco.player2_round_points += 1
        truco.play_cards = {}
        player1 = truco.player1_round_points
        player2 = truco.player2_round_points
        if player1 > player2 and player1 >= 2:
            truco.player1_points += truco.round_value
            truco.player1_round_points = 0
            truco.player2_round_points = 0
            round_finished = True
        elif player1 < player2 and player2 >= 2:
            truco.player2_points += truco.round_value
            truco.player1_round_points = 0
            truco.player2_round_points = 0
            round_finished = True
        elif player1 == player2 == 3:
            truco.player1_round_points = 0
            truco.player2_round_points = 0
            round_finished = True

        if truco.player1_points >= 12:
            game_finished = True
            truco.player1_game_points += 1
            truco.player1_points = 0
            truco.player2_points = 0
            if truco.player1_game_points >= 2:
                game_completed = True
        elif truco.player2_points >= 12:
            truco.player2_game_points += 1
            truco.player1_points = 0
            truco.player2_points = 0
            game_finished = True
            if truco.player1_game_points >= 2:
                game_completed = True

    async with context.db as db:
        if game_completed:
            await db.trucos.delete(game_id)
        else:
            await db.trucos.update(**truco.as_json(is_update=True))
            await db.session.refresh(truco)
    return ORJSONResponse(
        {
            "play_winner": play_winner,
            "round_finished": round_finished,
            "game_finished": game_finished,
            "game_completed": game_completed,
            "result": truco.as_json(),
        },
        status_code=200,
    )


@router.post("/ia/{game_id}/truco")
async def truco(
    game_id: int, schema: TrucoSchema, context: RequestContext = Depends(get_context)
):
    await assert_user_in_game(context, game_id)
    truco = await get_truco(context, game_id)
    if not truco:
        raise BadRequest(msg="Missing Entity")

    round_finished = False
    if schema.response:
        truco.round_value += 2
    else:
        truco.player1_points += truco.round_value
        truco.player1_round_points = 0
        truco.player2_round_points = 0
        round_finished = True

    game_finished = False
    game_completed = False
    if truco.player1_points >= 12:
        game_finished = True
        truco.player1_game_points += 1
        truco.player1_points = 0
        truco.player2_points = 0
        if truco.player1_game_points >= 2:
            game_completed = True

    async with context.db as db:
        if game_completed:
            await db.trucos.delete(game_id)
        else:
            await db.trucos.update(**truco.as_json(is_update=True))
            await db.session.refresh(truco)

    return ORJSONResponse(
        {
            "round_finished": round_finished,
            "game_finished": game_finished,
            "game_completed": game_completed,
            "result": truco.as_json(),
        },
        status_code=200,
    )
