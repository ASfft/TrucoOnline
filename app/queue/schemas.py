from pydantic import BaseModel


class JoinQueueSchema(BaseModel):
    game_mode: str
