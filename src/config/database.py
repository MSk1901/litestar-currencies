from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from src.config.settings import config

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=config.db.database_url, session_config=session_config
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
