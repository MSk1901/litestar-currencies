from litestar import Controller, get
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.currency.dto import CurrencyOutDto
from src.apps.currency.models import Currency
from src.apps.currency.repository import CurrencyRepository


class CurrencyController(Controller):
    @get(path="", return_dto=CurrencyOutDto)
    async def currency_list(self, db_session: AsyncSession) -> list[Currency]:
        """Список валют"""
        repo = CurrencyRepository(db_session)
        return await repo.get_currencies()
