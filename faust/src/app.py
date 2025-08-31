import os

import faust

KAFKA_HOST = os.environ.get("KAFKA_HOST", "kafka")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")


faust_app = faust.App(
    "currencies",
    broker=f"kafka://{KAFKA_HOST}:{KAFKA_PORT}",
    consumer_auto_offset_reset="earliest",
    topic_partitions=1,
)

from src.agents import cleanup_table, process_requests  # NOQA
