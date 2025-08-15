from faststream.rabbit import RabbitBroker

from src.config.settings import config

faststream_broker = RabbitBroker(config.rabbitmq.rabbitmq_url)
