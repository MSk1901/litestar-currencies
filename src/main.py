from litestar import Litestar

from src.config import faststream_broker, sqlalchemy_plugin

app = Litestar(
    plugins=[sqlalchemy_plugin],
    on_startup=[faststream_broker.start],
    on_shutdown=[faststream_broker.stop],
)
