from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.exceptions import register_exception_handlers
from app.middlewares import register_middlewares
from app.settings import Settings

from app.auth.routes import router as auth_router
from app.game.routes import router as game_router
from app.queue.routes import router as queue_router


def create_app(settings: Settings):
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # noinspection PyUnusedLocal
    @app.route("/")
    async def home(request):
        return ORJSONResponse({})

    register_exception_handlers(app, settings)
    register_middlewares(app, settings)

    app.include_router(auth_router, prefix=f"/auth")
    app.include_router(game_router, prefix=f"/game")
    app.include_router(queue_router, prefix=f"/queue")

    return app, settings
