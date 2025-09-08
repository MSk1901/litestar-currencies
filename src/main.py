from litestar import Litestar

from src.apps.datasource.tasks import fetch_rates_handler
from src.config import RequestAuditMiddleware, api_router, config, cors_config, faststream_broker
from src.config import lifespan as kafka_lifespan
from src.config import openapi_config, sqlalchemy_plugin

app = Litestar(
    debug=config.app.DEBUG,
    plugins=[sqlalchemy_plugin],
    lifespan=[kafka_lifespan],
    on_startup=[faststream_broker.start],
    on_shutdown=[faststream_broker.stop],
    openapi_config=openapi_config,
    route_handlers=[api_router],
    middleware=[RequestAuditMiddleware()],
    cors_config=cors_config,
)
