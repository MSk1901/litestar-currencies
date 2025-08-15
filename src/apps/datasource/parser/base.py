import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

import aiohttp

if TYPE_CHECKING:
    from src.apps.datasource.parser.dto import CurrencyDTO, CurrencyRateDTO

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    def __init__(self, data_source_url: str):
        self.data_source_url = data_source_url

    async def fetch(self, endpoint: str = "") -> Any:
        url = self.data_source_url + endpoint
        try:
            async with aiohttp.ClientSession() as client:
                response = await client.get(url)
        except Exception as e:
            logger.error(
                {
                    "message": "Произошла ошибка при обращении к внешнему сервису",
                    "url": url,
                    "exc": e,
                }
            )
        return response

    @abstractmethod
    async def parse_currencies(self) -> List["CurrencyDTO"]:
        pass

    @abstractmethod
    async def parse_rates(self) -> List["CurrencyRateDTO"]:
        pass
