from aiokafka import AIOKafkaConsumer

from src.common import CronRunner
from src.consumer.db_writer import DBWriter
from src.consumer.kafka_consumer import KafkaConsumer
from src.entities import Message


class PeriodicConsumer:
    def __init__(
        self,
        kafka_consumer_client: AIOKafkaConsumer,
        db_connection,
        cron_runner: CronRunner,
    ) -> None:
        self._consumer = KafkaConsumer(
            kafka_consumer_client, self.kafka_consumer_callback
        )
        self._writer = DBWriter(db_connection)
        self._cron_runner = cron_runner

    async def start(self) -> None:
        await self._writer.connect()

        await self._cron_runner.schedule(self._consumer.start, period=1)
        await self._cron_runner.schedule(self._writer.start, period=1)

    async def kafka_consumer_callback(self, message: Message) -> None:
        await self._writer.submit(message)
