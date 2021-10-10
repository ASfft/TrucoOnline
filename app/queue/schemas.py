from pydantic import BaseModel


class JoinQueueSchema(BaseModel):
    player_id: int
