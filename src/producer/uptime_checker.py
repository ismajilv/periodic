import logging
import re
import time
from contextlib import suppress
from typing import Optional

from aiohttp import ClientSession

from src.entities import CheckResult

LOGGER = logging.getLogger(__name__)


class UptimeChecker:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def check(
        self,
        site: str,
        regexp: Optional[str] = None,
        status_code: Optional[int] = 200,
    ) -> CheckResult:
        LOGGER.info(f"Checking {site}")

        with suppress(Exception):
            request_start_time = time.monotonic()
            async with self._session.get(site) as response:
                response_duration = time.monotonic() - request_start_time

                if response.status != status_code:
                    LOGGER.error(
                        f"Status code for site " f"{site} is {response.status}"
                    )
                    return CheckResult(
                        False,
                        f"Unexpected status code: {response.status}",
                        float("{:.2f}".format(response_duration)),
                    )

                if regexp:
                    content = await response.text()
                    response_duration = time.monotonic() - request_start_time
                    if not re.search(regexp, content):
                        LOGGER.error(f"Regexp {site} for site {site} not found")
                        return CheckResult(
                            False,
                            f"Regexp {regexp} not found",
                            float("{:.2f}".format(response_duration)),
                        )

            LOGGER.info(f"Site {site} is up")

            return CheckResult(True, None, float("{:.2f}".format(response_duration)))

        return CheckResult(False, "Unknown error", None)
