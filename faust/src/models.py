import faust


class RequestEvent(faust.Record, serializer="json"):
    ip: str
    endpoint: str
    params: dict
    body: dict


class WarningEvent(faust.Record, serializer="json"):
    ip: str
    count: int
    second: int
