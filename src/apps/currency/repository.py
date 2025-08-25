from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.currency.models import Currency


class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_currencies(self) -> list[Currency]:
        """Получение актуальных курсов"""
        async with self.session as session:
            result = await session.scalars(select(Currency).order_by(Currency.code))
            return list(result)
