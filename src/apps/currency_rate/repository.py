from datetime import date

from sqlalchemy import Select, Subquery, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.apps.currency.models import Currency
from src.apps.currency_rate.models import CurrencyRate


class CurrencyRateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _get_rates_subquery() -> Select:
        BaseCurrency = aliased(Currency)
        return (
            select(
                CurrencyRate.currency_id,
                CurrencyRate.base_currency_id,
                CurrencyRate.date,
                func.avg(CurrencyRate.value).label("rate"),
            )
            .join(BaseCurrency, CurrencyRate.base_currency_id == BaseCurrency.id)
            .where(BaseCurrency.code == "RUB")
            .where(CurrencyRate.value != 0)
            .group_by(CurrencyRate.currency_id, CurrencyRate.base_currency_id, CurrencyRate.date)
        )

    @staticmethod
    def _get_rates_query(subquery: Subquery) -> Select:
        return select(
            subquery.c.currency_id,
            subquery.c.date,
            subquery.c.rate,
            Currency.code.label("currency_code"),
        ).join(Currency, Currency.id == subquery.c.currency_id)

    async def get_actual_rates(self) -> list:
        """Получение актуальных курсов"""
        async with self.session as session:
            subquery = self._get_rates_subquery().where(CurrencyRate.is_actual.is_(True)).subquery()
            query = self._get_rates_query(subquery).order_by(Currency.code)
            result = await session.execute(query)
            return list(result)

    async def get_rates_history(self, start_date: date, end_date: date) -> list:
        """Получение истории курсов"""
        async with self.session as session:
            subquery = (
                self._get_rates_subquery()
                .where(CurrencyRate.date.between(start_date, end_date))
                .subquery()
            )
            query = self._get_rates_query(subquery).order_by(subquery.c.date, Currency.code)
            result = await session.execute(query)
            return list(result)
