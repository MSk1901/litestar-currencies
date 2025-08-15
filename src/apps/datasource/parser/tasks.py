import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.currency.models import Currency
from src.apps.currency_rate.models import CurrencyRate
from src.apps.datasource.models import DataSource
from src.apps.datasource.parser.cbr_parser import CbrParser
from src.apps.datasource.parser.constants import DataSourceEnum
from src.config.database import async_session
from src.config.faststream import faststream_broker

logger = logging.getLogger(__name__)


PARSER_MAPPING = {
    DataSourceEnum.CBR.name: CbrParser,
}


async def get_currencies(session: AsyncSession) -> None:
    currency_exists = await session.scalar(select(Currency))
    if currency_exists:
        return

    data_source = await session.scalar(select(DataSource).filter_by(name=DataSourceEnum.CBR))
    if not data_source:
        logger.error(f"No data source found for {DataSourceEnum.CBR.name} parser")
        return
    parser = CbrParser(str(data_source.url))

    currency_list = await parser.parse_currencies()
    filtered_currency_list = list({c.code: c for c in currency_list}.values())

    for currency in filtered_currency_list:
        currency_obj = Currency(**currency.model_dump())
        session.add(currency_obj)
        logger.info(f"Created currency {currency.code} in DB")


@faststream_broker.subscriber("fetch.cbr.rates")
async def fetch_rates_handler(data_source_name: str) -> None:
    async with async_session.begin() as session:
        source = await session.scalar(select(DataSource).filter_by(name=data_source_name))
        if not source:
            logger.warning(f"No data source with name {data_source_name} found")
            return

        await get_currencies(session)

        base_currency = await session.scalar(select(Currency).filter_by(code="RUB"))
        if not base_currency:
            base_currency = Currency(code="RUB", name="Российский рубль")
            session.add(base_currency)
        await session.flush()

        parser_class = PARSER_MAPPING.get(data_source_name)
        if not parser_class:
            logger.error(f"No parser found for {data_source_name} data source")
            return
        parser = parser_class(source.url)
        rate_list = await parser.parse_rates()
        for rate in rate_list:
            currency = await session.scalar(select(Currency).filter_by(code=rate.code))
            if not currency:
                logger.warning(f"No currency found for rate {rate.code}")
                continue

            await session.execute(
                update(CurrencyRate)
                .filter_by(
                    is_actual=True,
                    currency_id=currency.id,
                    data_source_id=source.id,
                    base_currency_id=base_currency.id,
                )
                .values(is_actual=False)
            )
            db_rate = CurrencyRate(
                currency_id=currency.id,
                value=rate.value,
                date=rate.date,
                base_currency_id=base_currency.id,
                data_source_id=source.id,
                is_actual=True,
            )
            logger.info(f"Added currency rate for {currency.code} from data source {source.name}")
            session.add(db_rate)
