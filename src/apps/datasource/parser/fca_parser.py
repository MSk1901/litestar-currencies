from datetime import date
from typing import List
from urllib.parse import urlencode

from src.apps.datasource.parser.base import BaseParser
from src.apps.datasource.parser.dto import CurrencyDTO, CurrencyRateDTO
from src.config.settings import config


class FCAParser(BaseParser):
    """Парсер данных о валютах и курсах от freecurrencyAPI"""

    API_KEY = config.app.FCA_API_KEY

    async def parse_currencies(self) -> List[CurrencyDTO]:
        """Парсинг валют"""

    async def parse_rates(self) -> List[CurrencyRateDTO]:
        """Парсинг курсов валют"""
        params = {"apikey": self.API_KEY, "base_currency": "RUB"}
        response = await self.fetch(f"latest?{urlencode(params)}")
        raw_data = await response.json()

        result = []
        for currency_code, rate in raw_data["data"].items():
            if currency_code == "RUB":
                continue
            result.append(CurrencyRateDTO(code=currency_code, date=date.today(), value=1 / rate))
        return result
