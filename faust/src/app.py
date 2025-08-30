import os

import faust

KAFKA_HOST = os.environ.get("KAFKA_HOST", "kafka")
KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")


faust_app = faust.App("currencies", broker=f"kafka://{KAFKA_HOST}:{KAFKA_PORT}")
