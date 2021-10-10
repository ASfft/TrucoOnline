from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.auth.schemas import LoginSchema
from app.context import RequestContext, get_context
from utils.constants import SESSION_COOKIE_NAME

router = APIRouter()


@router.post("/login")
async def login(schema: LoginSchema, context: RequestContext = Depends(get_context)):
    async with context.db as db:
        user = await db.users.login(schema.username, schema.password)
    response = ORJSONResponse({"user": user.as_json()})
    response.set_cookie(SESSION_COOKIE_NAME, user.id)
    return response


@router.post("/logout")
async def logout():
    response = ORJSONResponse({"msg": "Logout bem sucedido!", "status": 200}, status_code=200)
    response.set_cookie(SESSION_COOKIE_NAME, "", httponly=True, samesite="strict", expires=0)
    return response
