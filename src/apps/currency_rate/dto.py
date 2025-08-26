from pydantic import BaseModel


class CurrencyRateOutDto(BaseModel):
    currency_code: str
    rate: float


class ActualRatesOutDto(BaseModel):
    base: str = "RUB"
    rates: list[CurrencyRateOutDto]


class RatesHistoryOutDto(BaseModel):
    base: str = "RUB"
    rates: dict[str, list[CurrencyRateOutDto]]
