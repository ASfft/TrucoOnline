import asyncio
import inspect

import pytest
from fastapi import FastAPI

from app.databases.database import Database
from app.factory import create_app
from app.settings import Settings, get_settings
from tests.client import Client
from tests.utils import create_test_client
from utils.initialize import initialize_application, optimize_tables_for_testing


def pytest_collection_modifyitems(items):
    for item in items:
        if inspect.iscoroutinefunction(item.function):
            item.add_marker("asyncio")


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def settings() -> Settings:
    settings = Settings(debug_mode=True)
    yield settings
    await settings.close()


@pytest.fixture
async def db_session(settings: Settings):
    async with await settings.create_db_session() as session:
        yield session


@pytest.fixture
async def db(db_session):
    return Database(db_session)


@pytest.fixture(scope="session")
async def app(settings: Settings):
    app, settings = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    return app


@pytest.fixture(autouse=True)
async def clean_database(settings: Settings):
    await initialize_application(settings, flush_database=True, populate=False)


@pytest.fixture(autouse=True, scope="session")
async def optimizations():
    optimize_tables_for_testing()


@pytest.fixture
async def anon_user(app: FastAPI, settings: Settings, db: Database) -> Client:
    async with Client(app=app, user=None, settings=settings) as client:
        yield client


@pytest.fixture
async def user(app: FastAPI, settings: Settings, db: Database) -> Client:
    async with await create_test_client(app, settings, db) as client:
        yield client
