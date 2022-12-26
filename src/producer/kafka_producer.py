import logging

from aiokafka import AIOKafkaProducer

from src.entities import Message


LOGGER = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self._producer = kafka_producer

        super().__init__()

    async def start(self) -> None:
        await self._producer.start()

    async def produce(self, topic: str, message: Message) -> None:
        message_jsonb = message.to_jsonb()
        LOGGER.info(f"Producing {message_jsonb} to {topic}")
        await self._producer.send_and_wait(topic, message_jsonb)
