import unittest

from aiohttp import ClientSession
from aioresponses import aioresponses

from src.producer import UptimeChecker


class TestUptimeChecker(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session = ClientSession()
        self.checker = UptimeChecker(self.session)

    async def asyncTearDown(self) -> None:
        await self.session.close()

    @aioresponses()
    async def test_check_success_status_code(self, mock_aioresponse) -> None:
        # given
        site = "http://example.com"
        mock_aioresponse.get(site, status=200)

        # when
        result = await self.checker.check(site)

        # then
        self.assertTrue(result.up)
        self.assertIsNone(result.downtime_reason)
        self.assertIsNotNone(result.response_duration)

    @aioresponses()
    async def test_check_success_regexp(self, mock_aioresponse) -> None:
        # given
        site = "http://example.com"
        regexp = "Aierosponse"
        mock_aioresponse.get(site, status=200, body="Hello Aierosponse")

        # when
        result = await self.checker.check(site, regexp)

        # then
        self.assertTrue(result.up)
        self.assertIsNone(result.downtime_reason)
        self.assertIsNotNone(result.response_duration)

    @aioresponses()
    async def test_check_failure_status_code(self, mock_aioresponse) -> None:
        # given
        site = "http://example.com"
        mock_aioresponse.get(site, status=500)

        # when
        result = await self.checker.check(site)

        # then
        self.assertFalse(result.up)
        self.assertEqual(result.downtime_reason, "Unexpected status code: 500")
        self.assertIsNotNone(result.response_duration)

    @aioresponses()
    async def test_check_failure_regexp(self, mock_aioresponse) -> None:
        # given
        site = "http://example.com"
        regexp = "ANY"
        mock_aioresponse.get(site, status=200, body="Hello Aierosponse")

        # when
        result = await self.checker.check(site, regexp)

        # then
        self.assertFalse(result.up)
        self.assertEqual(result.downtime_reason, "Regexp ANY not found")
        self.assertIsNotNone(result.response_duration)

    @aioresponses()
    async def test_check_failure_any_exception(self, mock_aioresponse) -> None:
        # given
        site = "http://example.com"
        mock_aioresponse.get(site, exception=Exception("Any"))

        # when
        result = await self.checker.check(site)

        # then
        self.assertFalse(result.up)
        self.assertEqual(result.downtime_reason, "Unknown error")
        self.assertIsNone(result.response_duration)
