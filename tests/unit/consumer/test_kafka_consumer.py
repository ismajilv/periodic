import unittest
from datetime import datetime
from unittest.mock import AsyncMock

from aiokafka import AIOKafkaConsumer

from src.consumer import KafkaConsumer
from src.entities import Message


class TestKafkaConsumer(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.kafka_consumer = AsyncMock(spec=AIOKafkaConsumer)
        self.callback = AsyncMock()
        self.consumer = KafkaConsumer(self.kafka_consumer, self.callback)

    async def test_start(self) -> None:
        # given
        kafka_message = AsyncMock(
            value=b"{"
            b'"site": "http://example.com",'
            b'"checked_at": "2020-01-01T00:00:00",'
            b'"up": false,'
            b'"downtime_reason": "ConnectionError"'
            b"}"
        )
        self.kafka_consumer.__aiter__.return_value = [kafka_message]

        # when
        await self.consumer.start()

        # then
        self.callback.assert_called_once_with(
            Message(
                site="http://example.com",
                checked_at=datetime(2020, 1, 1, 0, 0),
                up=False,
                downtime_reason="ConnectionError",
            )
        )
