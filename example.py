import asyncio

from src.periodic import PeriodicChecker
from src.entities import PeriodicCheckerInput


async def main():
    input_ = PeriodicCheckerInput(
        site="https://testt.free.asdasdasd.com",
        period=2
    )

    await PeriodicChecker().start(periodic_checker_inputs=[input_])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
