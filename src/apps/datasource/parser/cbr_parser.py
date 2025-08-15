import xml.etree.ElementTree as ET
from datetime import date, datetime
from typing import List

from src.apps.datasource.parser.base import BaseParser
from src.apps.datasource.parser.dto import CurrencyDTO, CurrencyRateDTO


class CbrParser(BaseParser):
    """Парсер данных о валютах и курсах от CBR"""

    async def parse_currencies(self) -> List[CurrencyDTO]:
        """Парсинг валют"""
        response = await self.fetch("XML_valFull.asp")
        raw_data = await response.text()

        root = ET.fromstring(raw_data)
        result = []
        for currency in root.findall("Item"):
            code = currency.find("ISO_Char_Code").text
            name = currency.find("Name").text
            if not name or not code:
                continue
            result.append(CurrencyDTO(code=code, name=name))
        return result

    async def parse_rates(self) -> List[CurrencyRateDTO]:
        """Парсинг курсов валют"""
        response = await self.fetch("XML_daily.asp")
        raw_data = await response.text()

        root = ET.fromstring(raw_data)
        result = []
        _date = root.attrib.get("Date", date.today())
        if isinstance(_date, str):
            _date = datetime.strptime(_date, "%d.%m.%Y")
        for currency in root.findall("Valute"):
            code = currency.find("CharCode").text
            value = float(currency.find("VunitRate").text.replace(",", "."))
            result.append(CurrencyRateDTO(code=code, date=_date, value=value))
        return result
