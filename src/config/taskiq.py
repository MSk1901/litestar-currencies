from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler

from src.apps.datasource.constants import DataSourceEnum
from src.config.faststream import faststream_broker

taskiq_broker = BrokerWrapper(faststream_broker)

taskiq_broker.task(
    message=DataSourceEnum.CBR,
    queue="fetch.cbr.rates",
    schedule=[
        {
            "cron": "0 1 * * *",
        }
    ],
)

taskiq_broker.task(
    message=DataSourceEnum.FCA,
    queue="fetch.fca.rates",
    schedule=[
        {
            "cron": "5 1 * * *",
        }
    ],
)

scheduler = StreamScheduler(
    broker=taskiq_broker,
    sources=[LabelScheduleSource(taskiq_broker)],
)
