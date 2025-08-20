from litestar import Litestar

from src.apps.datasource.tasks import fetch_rates_handler
from src.config import api_router, faststream_broker, openapi_config, sqlalchemy_plugin

app = Litestar(
    plugins=[sqlalchemy_plugin],
    on_startup=[faststream_broker.start],
    on_shutdown=[faststream_broker.stop],
    openapi_config=openapi_config,
    route_handlers=[api_router],
)
