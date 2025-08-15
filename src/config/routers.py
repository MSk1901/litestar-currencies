from litestar import Router

from apps.currency_rate.routers import rate_router

api_router = Router(path="/api", route_handlers=[rate_router])
