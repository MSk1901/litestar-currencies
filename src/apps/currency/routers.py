from litestar import Router

from src.apps.currency.controllers import CurrencyController

currency_router = Router(path="/currencies", tags=["Валюты"], route_handlers=[CurrencyController])
