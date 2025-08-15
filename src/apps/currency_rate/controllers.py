from litestar import Controller, get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.currency_rate.dto import CurrencyRateOutDto
from src.apps.currency_rate.models import CurrencyRate


class CurrencyRateController(Controller):
    path = "/rate"

    @get(path="/actual")
    async def get_actual_rates(self, db_session: AsyncSession) -> list[CurrencyRateOutDto]:
        """Актуальные курсы валют"""
        rates = await db_session.scalars(
            select(CurrencyRate)
            .filter_by(is_actual=True)
            .options(joinedload(CurrencyRate.currency))
        )
        return [
            CurrencyRateOutDto(currency_code=rate.currency.code, rate=float(rate.value))
            for rate in rates
        ]
