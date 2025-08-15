from datetime import date

from pydantic import BaseModel


class CurrencyDTO(BaseModel):
    code: str
    name: str
    symbol: str = None


class CurrencyRateDTO(BaseModel):
    code: str
    value: float
    date: date
