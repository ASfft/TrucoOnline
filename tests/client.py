import httpx
from fastapi import FastAPI
from httpx import AsyncClient

from app.settings import Settings


class Client(AsyncClient):
    def __init__(
        self,
        user,
        settings: Settings,
        app: FastAPI,
        password: str = None,
        ip_address: str = "127.0.0.1",
        *args,
        **kwargs,
    ):
        if user:
            kwargs["headers"] = kwargs.get("headers", {})
            kwargs["headers"]["Authorization"] = f"Bearer {user.id}"
        transport = httpx.ASGITransport(
            app=app, raise_app_exceptions=True, client=(ip_address, 80)
        )
        super().__init__(
            *args, **kwargs, app=app, base_url="http://test", transport=transport
        )
        self.user = user
        self.password = password
        self.settings = settings
        self.app = app
