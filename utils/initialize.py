import asyncio
import logging

from app.factory import create_app
from app.models import Base
from app.settings import Settings, get_settings


def optimize_tables_for_testing():
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    for table in Base.metadata.sorted_tables:
        table.__table_args__ = {"prefixes": ["UNLOGGED"]}


async def flush_everything(settings: Settings):
    logging.info("Re-creating all tables...")
    async with settings.db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def initialize_application(settings, flush_database: bool, populate: bool = True):
    if flush_database:
        await flush_everything(settings)
    async with await settings.create_db_session() as session:
        await session.commit()


async def main():
    app, settings_ = create_app(get_settings())
    conditions = (
        settings_.debug_mode,
        settings_.pg_host.startswith(("127.0.0.1", "localhost")),
    )
    if all(conditions):
        await initialize_application(settings_, flush_database=True)
        print("Initialized successfully")
    else:
        print("This do not seems a dev environment, refusing to initialize.")


if __name__ == "__main__":
    asyncio.run(main())
