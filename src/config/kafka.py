from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer

from src.config.settings import config


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator[dict, None]:
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{config.kafka.KAFKA_HOST}:{config.kafka.KAFKA_PORT}"
    )
    try:
        await producer.start()
        app.state.kafka_producer = producer
        yield {"producer": producer}
    finally:
        await producer.stop()
