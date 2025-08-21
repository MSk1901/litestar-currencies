from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.currency.models import Currency
from src.apps.currency_rate.models import CurrencyRate


class CurrencyRateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_actual_rates(self) -> list:
        """Получение актуальных курсов"""
        async with self.session as session:
            subquery = (
                select(
                    CurrencyRate.currency_id,
                    CurrencyRate.base_currency_id,
                    CurrencyRate.date,
                    func.avg(CurrencyRate.value).label("rate"),
                )
                .where(CurrencyRate.is_actual.is_(True))
                .where(CurrencyRate.value != 0)
                .group_by(
                    CurrencyRate.currency_id, CurrencyRate.base_currency_id, CurrencyRate.date
                )
                .subquery()
            )
            query = (
                select(
                    subquery.c.currency_id,
                    subquery.c.base_currency_id,
                    subquery.c.date,
                    subquery.c.rate,
                    Currency.code.label("currency_code"),
                )
                .join(Currency, Currency.id == subquery.c.currency_id)
                .order_by(Currency.code)
            )
            result = await session.execute(query)
            return list(result)
