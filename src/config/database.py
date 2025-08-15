from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
    base,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config.settings import config

Base = base.UUIDAuditBase

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=config.db.database_url,
    create_all=True,
    metadata=Base.metadata,
    session_config=session_config,
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)


engine = create_async_engine(config.db.database_url, echo=config.db.ENABLE_ECHO)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
