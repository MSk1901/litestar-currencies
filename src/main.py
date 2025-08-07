from litestar import Litestar

from src.config import sqlalchemy_plugin

app = Litestar(plugins=[sqlalchemy_plugin])
