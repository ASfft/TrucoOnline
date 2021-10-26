from fastapi import FastAPI, Request
from sqlalchemy import select

from app.models import User
from .databases.database import Database

from .settings import Settings


def register_middlewares(app: FastAPI, settings: Settings):
    @app.middleware("http")
    async def authorize_request(request: Request, call_next):

        session = await settings.create_db_session()
        request.state.db_session = session
        request.state.db = Database(session)
        request.state.settings = settings

        auth_header = request.headers.get("Authorization", "")
        token = auth_header[auth_header.find("Bearer") + 7 :]

        if token:
            query = select(User).where(User.id == int(token))
            user = (await session.execute(query)).scalars().first()
            request.state.user = user
            return await call_next(request)

        return await call_next(request)

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
