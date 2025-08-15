from pydantic import BaseModel


class CurrencyRateOutDto(BaseModel):
    currency_code: str
    rate: float
