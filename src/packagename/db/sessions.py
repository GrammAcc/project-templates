import asyncio

from sqlalchemy import insert, event
from sqlalchemy.pool import ConnectionPoolEntry
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from . import models


_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
_Session = async_scoped_session(
    async_sessionmaker(bind=_engine, expire_on_commit=False),
    scopefunc=asyncio.current_task,
)


def _enable_sqlite_fks(
    dbapi_con: DBAPIConnection, connection_record: ConnectionPoolEntry
):
    """SQLite3 does not enable foreign key constraints by default.
    We have to enable them with a pragma query, but this will cause errors
    in other backends, so we check that we are connected to a SQLite db before
    sending the pragma."""

    if _engine.dialect.name == "sqlite":
        dbapi_con.cursor().execute("PRAGMA foreign_keys = ON;")


event.listen(_engine.sync_engine, "connect", _enable_sqlite_fks)


async def _create_all(drop: bool = False) -> None:
    """Create all declarative tables.

    If `drop` is True, drop all tables and data before recreating the tables.
    """

    async with _engine.begin() as conn:
        if drop:
            await conn.run_sync(models.BaseModel.metadata.drop_all)
        await conn.run_sync(models.BaseModel.metadata.create_all)


async def _seed() -> None:
    """Seed the database."""

    print("Seeding the database...")
    await _create_all(drop=True)
    async with _Session() as session:
        example1 = models.Example(id=1, name="Some Example")
        example2 = models.Example(id=2, name="Some Other Example")
        mtmexample = models.MTMExample(id=1, name="Some Many-to-Many Example")
        otmexample = models.OTMExample(
            id=1, example_id=example1.id, name="Some One-to-Many Example"
        )
        session.add_all(
            [
                example1,
                example2,
                mtmexample,
                otmexample,
            ]
        )
        await session.commit()
        await session.execute(
            insert(models.table_example_mtmexample).values(
                example_id=example2.id, mtmexample_id=mtmexample.id
            )
        )
        await session.commit()
    print("Db seed complete!")


def _connect(db_uri: str, debug: bool = False) -> None:
    """Update the sqlalchemy async engine and scoped session to connect to
    the db at `db_uri`.

    If `seed` is True, then also seed the db at the new connection.
    If `debug` is True, then emit generated sql.
    """

    global _engine
    global _Session
    _engine = create_async_engine(db_uri, echo=debug)
    _Session = async_scoped_session(
        async_sessionmaker(bind=_engine, expire_on_commit=False),
        scopefunc=asyncio.current_task,
    )
    event.listen(_engine.sync_engine, "connect", _enable_sqlite_fks)


def get_session() -> AsyncSession:
    return _Session()


def get_session_proxy() -> async_scoped_session:
    return _Session
