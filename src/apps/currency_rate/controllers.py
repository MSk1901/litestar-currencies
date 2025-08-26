from collections import defaultdict
from datetime import date

from litestar import Controller, get
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.currency_rate.dto import ActualRatesOutDto, CurrencyRateOutDto, RatesHistoryOutDto
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

    @get(path="/history")
    async def rates_history(
        self, start_date: date, end_date: date, db_session: AsyncSession
    ) -> RatesHistoryOutDto:
        """Актуальные курсы валют"""
        repo = CurrencyRateRepository(db_session)
        rates = await repo.get_rates_history(start_date, end_date)
        rates_by_date = defaultdict(list)
        for rate in rates:
            date_str = rate.date.strftime("%d.%m.%Y")
            rates_by_date[date_str].append(
                CurrencyRateOutDto(currency_code=rate.currency_code, rate=float(rate.rate))
            )
        return RatesHistoryOutDto(rates=rates_by_date)
