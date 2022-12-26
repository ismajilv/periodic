import unittest
from datetime import datetime
from unittest.mock import AsyncMock

from aiokafka import AIOKafkaProducer

from src.entities import Message
from src.producer import KafkaProducer


class TestKafkaProducer(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.kafka_producer = AsyncMock(spec=AIOKafkaProducer)
        self.producer = KafkaProducer(self.kafka_producer)

    async def test_start(self) -> None:
        # when
        await self.producer.start()

        # then
        self.kafka_producer.start.assert_awaited_once()

    async def test_produce(self) -> None:
        # given
        datetime_ = datetime(2020, 1, 1, 0, 0, 0)
        topic = "test"
        message = Message(
            site="http://example.com",
            checked_at=datetime_,
            up=True,
            downtime_reason=None,
        )

        # when
        await self.producer.produce(topic, message)

        # then
        self.kafka_producer.send_and_wait.assert_awaited_once_with(
            topic,
            b'{"site": "http://example.com", "up": true, '
            b'"downtime_reason": null, '
            b'"checked_at": "2020-01-01T00:00:00"}'
        )
