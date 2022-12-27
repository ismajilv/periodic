import logging
from typing import List

import asyncpg
from aiohttp import ClientSession
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

import settings
from src.common import CronRunner
from src.consumer import PeriodicConsumer
from src.entities import PeriodicCheckerInput
from src.producer import PeriodicProducer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class PeriodicChecker:
    def __init__(self) -> None:
        self._tasks = []

        kafka_consumer_client = AIOKafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        )
        kafka_producer_client = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        )
        db_connection = asyncpg.connect(
            dsn=settings.DB_DSN,
        )
        session = ClientSession()
        cron_runner = CronRunner()

        self._periodic_producer = PeriodicProducer(
            kafka_producer_client=kafka_producer_client,
            topic=settings.KAFKA_TOPIC,
            session=session,
            cron_runner=cron_runner,
        )
        self._periodic_consumer = PeriodicConsumer(
            kafka_consumer_client=kafka_consumer_client,
            db_connection=db_connection,
            cron_runner=cron_runner,
        )

    async def start(self, periodic_checker_inputs: List[PeriodicCheckerInput]) -> None:
        if not periodic_checker_inputs:
            LOGGER.warning("No checks defined, exiting")
            return

        await self._periodic_producer.start(periodic_checker_inputs)
        await self._periodic_consumer.start()
