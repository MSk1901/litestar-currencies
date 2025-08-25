from litestar import Router

from src.apps.currency_rate.controllers import CurrencyRateController

rate_router = Router(path="/rates", tags=["Курсы валют"], route_handlers=[CurrencyRateController])
