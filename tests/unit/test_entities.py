import unittest
from datetime import datetime

from src.entities import Message


class TestMessage(unittest.TestCase):

    def setUp(self) -> None:
        datetime_ = datetime(2020, 1, 1, 0, 0, 0)

        self.jsonb = \
            b'{"site": "http://example.com", ' \
            b'"up": true, ' \
            b'"downtime_reason": "Error", ' \
            b'"checked_at": "2020-01-01T00:00:00"}'
        self.message = Message(
            site="http://example.com",
            up=True,
            downtime_reason="Error",
            checked_at=datetime_
        )

    def test_to_jsonb(self):
        # when
        jsonb = self.message.to_jsonb()

        # then
        self.assertEqual(jsonb, self.jsonb)

    def test_from_jsonb(self):
        # when
        message = Message.from_jsonb(self.jsonb)

        # then
        self.assertEqual(message, self.message)
