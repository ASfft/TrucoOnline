from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from shortuuid import uuid

from app.auth.schemas import LoginSchema
from app.context import RequestContext, get_context

router = APIRouter()


@router.post("/login")
async def login(schema: LoginSchema, context: RequestContext = Depends(get_context)):
    async with context.db as db:
        user = await db.users.login(schema.username, schema.password)
    response = ORJSONResponse({"user": user.as_json()})
    return response


@router.post("/register")
async def register(schema: LoginSchema, context: RequestContext = Depends(get_context)):
    async with context.db as db:
        user = await db.users.add(schema.username, schema.password)
    response = ORJSONResponse({"user": user.as_json()})
    return response


@router.get("/anon")
async def anon_register(context: RequestContext = Depends(get_context)):
    async with context.db as db:
        user = await db.users.add(uuid(), uuid())
    response = ORJSONResponse({"user": user.as_json()})
    return response
