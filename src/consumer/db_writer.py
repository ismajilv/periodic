import logging

from typing import List

from src.common import QueueBasedWorker
from src.entities import Message


LOGGER = logging.getLogger(__name__)


INSERT_CHECK_QUERY = """
    INSERT INTO checks (site, up, downtime_reason, checked_at)
    VALUES ($1, $2, $3, $4)
"""


class DBWriter(QueueBasedWorker):
    def __init__(self, connection):
        self._connection = connection

        super().__init__()

    async def connect(self):
        self._connection = await self._connection

    async def _start(self):
        messages: List[Message] = await self.get_all()

        if messages:
            insert_values = []
            for message in messages:
                insert_value = (
                    message.site,
                    message.up,
                    message.downtime_reason,
                    message.checked_at,
                )
                insert_values.append(insert_value)
            await self._connection.executemany(
                INSERT_CHECK_QUERY,
                insert_values
            )
            LOGGER.info("Successfully inserted all messages from queue to DB")
