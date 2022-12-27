import unittest
from datetime import datetime

import asyncpg

from decouple import config
from src.consumer import DBWriter
from src.entities import Message


class TestDBWriter(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.connection = await asyncpg.connect(
            dsn=config("DB_DSN"),
        )
        self.writer = DBWriter(self.connection)

    async def asyncTearDown(self) -> None:
        await self.writer._connection.execute("DELETE FROM checks")
        await self.writer._connection.close()

    async def test_insert_message(self):
        # given
        message = Message(
            site="test",
            up=True,
            downtime_reason=None,
            response_duration=0.1,
            checked_at=datetime(2021, 1, 1, 1, 1, 1),
        )

        # when
        await self.writer.submit(message)
        await self.writer.start()

        # then
        result = await self.writer._connection.fetchrow("SELECT * FROM checks")
        self.assertEqual(result["site"], "test")
        self.assertEqual(result["up"], True)
        self.assertEqual(result["downtime_reason"], None)
        self.assertEqual(result["response_duration"], 0.1)
        self.assertEqual(result["checked_at"], datetime(2021, 1, 1, 1, 1, 1))
