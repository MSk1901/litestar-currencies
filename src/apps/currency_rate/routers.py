from litestar import Router

from src.apps.currency_rate.controllers import CurrencyRateController

rate_router = Router(path="", route_handlers=[CurrencyRateController])
