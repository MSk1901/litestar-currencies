import json

from litestar import Request
from litestar.enums import ScopeType
from litestar.middleware import ASGIMiddleware
from litestar.types import ASGIApp, Message, Receive, Scope, Send


class RequestAuditMiddleware(ASGIMiddleware):
    scopes = (ScopeType.HTTP, ScopeType.ASGI)

    async def handle(self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp) -> None:
        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                producer = scope["app"].state.kafka_producer
                request = Request(scope)
                endpoint = scope["path"]
                ip = scope["client"][0] if scope.get("client") else None

                # Собираем параметры (query + body)
                json_body = None
                params = dict(request.query_params)
                if request.method in ("POST", "PUT", "PATCH"):
                    try:
                        json_body = await request.json()
                    except Exception:
                        json_body = None

                msg = {
                    "ip": ip,
                    "endpoint": endpoint,
                    "params": params,
                    "body": json_body,
                }

                await producer.send_and_wait(topic="request.audit", value=json.dumps(msg).encode())

            await send(message)

        await next_app(scope, receive, send_wrapper)
