from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from app.settings import Settings


class BadRequest(Exception):
    def __init__(self, msg: str = None, status_code: int = 400, *args, **kwargs):
        self.msg = msg
        self.status_code = status_code
        self.args = args
        self.kwargs = kwargs


def register_exception_handlers(app: FastAPI, settings: Settings):
    @app.exception_handler(BadRequest)
    async def handle_bad_request(request: Request, exc: BadRequest):
        return ORJSONResponse({"msg": exc.msg, "status": 400, **exc.kwargs}, status_code=exc.status_code)
