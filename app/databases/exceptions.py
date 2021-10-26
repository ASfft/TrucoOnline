from app.exceptions import BadRequest


class WrongCredentials(BadRequest):
    def __init__(self):
        super().__init__(msg="Dados inválidos")


class AlreadyInGame(BadRequest):
    def __init__(self, game_id: int):
        super().__init__(msg="Já está em um jogo!", game_id=str(game_id))


class GamePlayersLimitExceed(BadRequest):
    def __init__(self):
        super().__init__(msg="O jogo suporta apenas 3 jogadores.")
