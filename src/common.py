import asyncio
import logging

from abc import abstractmethod
from typing import List

from src.entities import Message

LOGGER = logging.getLogger(__name__)


class QueueExtended(asyncio.Queue):
    async def get_all(self) -> List[Message]:
        items = []
        while self.qsize():
            item = await self.get()
            items.append(item)

        return items


class QueueBasedWorker:
    def __init__(self):
        self._queue = QueueExtended()

    async def submit(self, message: Message) -> None:
        await self._queue.put(message)

    async def get_all(self) -> List[Message]:
        return await self._queue.get_all()

    async def start(self) -> None:
        try:
            await self._start()
        except Exception as ex:
            LOGGER.error("Error occurred in worker", exc_info=ex)

    @abstractmethod
    async def _start(self) -> None:
        raise NotImplementedError()


class CronRunner:
    def __init__(self):
        self._tasks: List[asyncio.Task] = []

    async def schedule(self, coro, *args, period: int) -> None:
        async def cron_runner(coro_, *args_, period_: int) -> None:
            while True:
                await coro_(*args_)
                await asyncio.sleep(period_)

        coro = cron_runner(coro, *args, period_=period)
        task = asyncio.create_task(coro)
        self._tasks.append(task)
