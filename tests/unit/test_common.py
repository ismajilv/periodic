import unittest
from unittest.mock import MagicMock

from src.common import QueueExtended
from src.entities import Message


class TestQueueExtended(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.queue = QueueExtended()

    async def test_get_all(self):
        # given
        message_1 = MagicMock(spec=Message)
        message_2 = MagicMock(spec=Message)
        await self.queue.put(message_1)
        await self.queue.put(message_2)

        # when
        messages = await self.queue.get_all()

        # then
        self.assertEqual(messages, [message_1, message_2])

