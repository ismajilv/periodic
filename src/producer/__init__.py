from datetime import datetime
from typing import List

from aiohttp import ClientSession
from aiokafka import AIOKafkaProducer

from src.common import CronRunner
from src.entities import Message, PeriodicCheckerInput
from src.producer.kafka_producer import KafkaProducer
from src.producer.uptime_checker import UptimeChecker


class PeriodicProducer:
    def __init__(
        self,
        kafka_producer_client: AIOKafkaProducer,
        topic: str,
        session: ClientSession,
        cron_runner: CronRunner,
    ) -> None:
        self._producer = KafkaProducer(kafka_producer_client)
        self._uptime_checker = UptimeChecker(session)
        self._cron_runner = cron_runner
        self._topic = topic

    async def start(self, periodic_checker_inputs: List[PeriodicCheckerInput]) -> None:
        await self._producer.start()
        for periodic_checker_input in periodic_checker_inputs:
            await self._cron_runner.schedule(
                self._check_uptime_and_produce_metrics_to_kafka,
                periodic_checker_input.site,
                periodic_checker_input.regexp,
                periodic_checker_input.status_code,
                period=periodic_checker_input.period,
            )

    async def _check_uptime_and_produce_metrics_to_kafka(
        self, site: str, regexp: str, status_code: int
    ) -> None:
        check_result = await self._uptime_checker.check(
            site=site,
            regexp=regexp,
            status_code=status_code,
        )
        message = Message(
            up=check_result.up,
            checked_at=datetime.utcnow(),
            site=site,
            downtime_reason=check_result.downtime_reason,
            response_duration=check_result.response_duration,
        )
        await self._producer.produce(self._topic, message)
