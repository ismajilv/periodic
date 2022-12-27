import asyncio
from contextlib import asynccontextmanager
from typing import List

import asyncpg
import pytest

import settings
from src.entities import PeriodicCheckerInput
from src.periodic import PeriodicChecker


async def periodic_run(input_: List[PeriodicCheckerInput]) -> None:
    periodic = PeriodicChecker()
    await periodic.start(periodic_checker_inputs=input_)


@asynccontextmanager
async def setup_and_cleanup():
    connection = await asyncpg.connect(
        dsn=settings.DB_DSN,
    )

    yield connection

    await connection.execute("DELETE FROM checks;")


@pytest.mark.asyncio
async def test_success():
    async with setup_and_cleanup() as connection:
        # given
        input_ = PeriodicCheckerInput(site="https://www.google.com", period=1)

        # when
        loop = asyncio.get_event_loop()
        loop.create_task(periodic_run([input_]))

        # then
        await asyncio.sleep(4)
        rows = await connection.fetch("SELECT * FROM checks;")
        rows_dict = [dict(row) for row in rows]
        assert rows_dict[0]["site"] == "https://www.google.com"
        assert rows_dict[0]["up"] is True


@pytest.mark.asyncio
async def test_failure():
    async with setup_and_cleanup() as connection:
        # given
        input_ = PeriodicCheckerInput(site="https://testt.free.asdasdasd.com", period=1)

        # when
        loop = asyncio.get_event_loop()
        loop.create_task(periodic_run([input_]))

        # then
        await asyncio.sleep(5)
        rows = await connection.fetch("SELECT * FROM checks;")
        rows_dict = [dict(row) for row in rows]
        assert rows_dict[0]["site"] == "https://testt.free.asdasdasd.com"
        assert rows_dict[0]["up"] is False
