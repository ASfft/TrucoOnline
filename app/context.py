from dataclasses import dataclass
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.databases.database import Database
from app.models import User
from app.settings import Settings


@dataclass
class RequestContext:
    request: Request
    extra: dict
    db_session: AsyncSession
    db: Database
    settings: Settings
    user: Optional[User] = None

    @classmethod
    def from_request(cls, request: Request, **kwargs):
        settings: Settings = request.state.settings
        try:
            user = request.state.user
        except AttributeError:
            user = None

        return cls(
            extra=kwargs,
            db_session=request.state.db_session,
            db=request.state.db,
            user=user,
            request=request,
            settings=settings,
        )


async def get_context(request: Request) -> RequestContext:
    return RequestContext.from_request(request)
