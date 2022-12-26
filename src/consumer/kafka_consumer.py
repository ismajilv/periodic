import logging

from aiokafka import AIOKafkaConsumer

from src.common import QueueBasedWorker
from src.entities import Message

LOGGER = logging.getLogger(__name__)


class KafkaConsumer(QueueBasedWorker):
    def __init__(self, kafka_consumer: AIOKafkaConsumer, callback: callable):
        self._consumer = kafka_consumer
        self._callback = callback

        super().__init__()

    async def _start(self) -> None:
        await self._consumer.start()

        async for kafka_msg in self._consumer:
            LOGGER.info(f"Consuming message {kafka_msg} from Kafka")
            message = Message.from_jsonb(kafka_msg.value)
            await self._callback(message)

        await self._consumer.stop()
