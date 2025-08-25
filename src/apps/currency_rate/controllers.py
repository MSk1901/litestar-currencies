from litestar import Controller, get
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.currency_rate.dto import ActualRatesOutDto, CurrencyRateOutDto
from src.apps.currency_rate.repository import CurrencyRateRepository


class CurrencyRateController(Controller):
    @get(path="/actual")
    async def actual_rates(self, db_session: AsyncSession) -> ActualRatesOutDto:
        """Актуальные курсы валют"""
        repo = CurrencyRateRepository(db_session)
        rates = await repo.get_actual_rates()
        return ActualRatesOutDto(
            rates=[
                CurrencyRateOutDto(currency_code=rate.currency_code, rate=float(rate.rate))
                for rate in rates
            ]
        )
