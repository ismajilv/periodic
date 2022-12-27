import unittest
from datetime import datetime
from unittest.mock import AsyncMock

from src.consumer import DBWriter
from src.consumer.db_writer import INSERT_CHECK_QUERY
from src.entities import Message


class TestDBWriter(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.connection = AsyncMock()
        self.db_writer = DBWriter(self.connection)

    async def test_start_without_message(self) -> None:
        # given
        self.db_writer.get_all = AsyncMock(return_value=[])

        # when
        await self.db_writer.start()

        # then
        self.assertFalse(self.connection.executemany.called)

    async def test_start_with_message(self) -> None:
        # given
        datetime_ = datetime(2020, 1, 1, 0, 0, 0)
        message = Message(
            site="http://example.com", response_duration=0.1, checked_at=datetime_
        )
        self.db_writer.get_all = AsyncMock(return_value=[message])

        # when
        await self.db_writer.start()

        # then
        self.connection.executemany.assert_awaited_once_with(
            INSERT_CHECK_QUERY, [("http://example.com", None, None, 0.1, datetime_)]
        )
