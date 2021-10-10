import httpx
from fastapi import FastAPI
from httpx import AsyncClient

from app.settings import Settings
from utils.constants import SESSION_COOKIE_NAME


class Client(AsyncClient):
    def __init__(self, user, settings: Settings, app: FastAPI, password: str = None,
                 ip_address: str = "127.0.0.1", *args, **kwargs):
        kwargs["cookies"] = kwargs.get("cookies", {})
        kwargs["cookies"][SESSION_COOKIE_NAME] = str(user.id) if user else ""
        transport = httpx.ASGITransport(app=app, raise_app_exceptions=True, client=(ip_address, 80))
        super().__init__(*args, **kwargs, app=app, base_url="http://test", transport=transport)
        self.user = user
        self.password = password
        self.settings = settings
        self.app = app
