import asyncio
import unittest
from datetime import datetime
from unittest.mock import AsyncMock

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from decouple import config

from src.consumer import KafkaConsumer
from src.entities import Message
from src.producer import KafkaProducer


class TestKafkaProducer(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.topic = config("KAFKA_TOPIC")

        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=config("KAFKA_BOOTSTRAP_SERVERS")
        )
        self.kafka_consumer = AIOKafkaConsumer(
            self.topic, bootstrap_servers=config("KAFKA_BOOTSTRAP_SERVERS")
        )
        self.callback = AsyncMock()
        self.producer = KafkaProducer(self.kafka_producer)
        self.consumer = KafkaConsumer(self.kafka_consumer, self.callback)
        await self.producer.start()

    async def test_produce(self):
        # given
        message = Message(
            site="test",
            up=True,
            downtime_reason=None,
            response_duration=0.1,
            checked_at=datetime(2021, 1, 1, 1, 1, 1),
        )

        # when
        loop = asyncio.get_event_loop()
        loop.create_task(self.consumer._start())
        await asyncio.sleep(1)
        await self.producer.produce(self.topic, message)
        await asyncio.sleep(1)

        # then
        self.callback.assert_awaited_once_with(message)
