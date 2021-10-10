from typing import Optional

import re
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import select

from app.models import User
from utils.constants import SESSION_COOKIE_NAME
from .databases.database import Database

from .settings import Settings

UNAUTHENTICATED_PATHS = {
    "/",
    "/auth/login",
}


def register_middlewares(app: FastAPI, settings: Settings):
    @app.middleware("http")
    async def authorize_request(request: Request, call_next):

        session = await settings.create_db_session()
        request.state.db_session = session
        request.state.db = Database(session)
        request.state.settings = settings

        try:
            token = int(request.cookies.get(SESSION_COOKIE_NAME))
        except ValueError:
            token = None

        if token:
            query = (select(User).where(User.id == token))
            user: Optional[User] = (await session.execute(query)).scalars().first()

            if user:
                request.state.user = user
                return await call_next(request)

        # Checking if this is a public request and should be allowed anyway.
        if request.url.path in UNAUTHENTICATED_PATHS:
            return await call_next(request)

        response = ORJSONResponse(
            {"msg": "Não autorizado", "status": 401}, status_code=401
        )
        response.set_cookie(SESSION_COOKIE_NAME, httponly=True, samesite="strict", expires=0)
        return response

    @app.middleware("http")
    async def close_db_session(request: Request, call_next):
        response = None
        try:
            response = await call_next(request)
        except Exception as error:
            raise error
        finally:
            try:
                if request.state.db_session:
                    await request.state.db_session.close()
            except AttributeError:
                pass
        return response
