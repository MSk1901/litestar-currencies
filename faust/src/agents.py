import time

from src.app import faust_app
from src.models import WarningEvent
from src.topics import request_topic, warning_topic
from src.utils import get_current_minute_interval

request_count = faust_app.Table("requests_per_ip_per_minute", default=int)
last_alerted = faust_app.Table("last_alerted_per_ip", default=int)


@faust_app.agent(request_topic)
async def process_requests(stream):
    async for event in stream:
        now = time.time()
        minute_key = get_current_minute_interval(now)
        interval_key = get_current_minute_interval(now, 10)
        ip = event["ip"]
        key = (ip, minute_key)
        request_count[key] += 1
        if request_count[key] > 1000 and last_alerted[ip] != interval_key:
            warning = WarningEvent(ip=event["ip"], count=request_count[key], second=minute_key)
            await warning_topic.send(value=warning)
            last_alerted[ip] = interval_key


@faust_app.timer(interval=60.0)
async def cleanup_table():
    current_minute = get_current_minute_interval(faust_app.loop.time())
    min_to_keep = set()
    for ip, minute in request_count.keys():
        if minute >= current_minute - 120:
            min_to_keep.add((ip, minute))
    to_delete = [k for k in request_count.keys() if k not in min_to_keep]
    for k in to_delete:
        del request_count[k]
