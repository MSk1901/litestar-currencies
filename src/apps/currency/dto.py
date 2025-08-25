from litestar.dto import DTOConfig
from litestar.plugins.sqlalchemy import SQLAlchemyDTO

from src.apps.currency.models import Currency


class CurrencyOutDto(SQLAlchemyDTO[Currency]):
    config = DTOConfig(include={"name", "code"})
