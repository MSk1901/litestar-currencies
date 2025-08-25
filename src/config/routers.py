from litestar import Router

from src.apps.currency.routers import currency_router
from src.apps.currency_rate.routers import rate_router

api_router = Router(path="/api", route_handlers=[rate_router, currency_router])
