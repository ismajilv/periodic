import logging
from typing import List

import asyncpg
from aiohttp import ClientSession
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from decouple import config

from src.common import CronRunner
from src.consumer import PeriodicConsumer
from src.entities import PeriodicCheckerInput
from src.producer import PeriodicProducer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class PeriodicChecker:

    CONFIG: dict = {
        "kafka": {
            "topic": config("KAFKA_TOPIC"),
            "bootstrap_servers": config("KAFKA_BOOTSTRAP_SERVERS"),
        },
        "db": {
            "dsn": config("DB_DSN"),
        },
    }

    def __init__(self) -> None:
        self._tasks = []

        kafka_consumer_client = AIOKafkaConsumer(
            self.CONFIG["kafka"]["topic"],
            bootstrap_servers=self.CONFIG["kafka"]["bootstrap_servers"],
        )
        kafka_producer_client = AIOKafkaProducer(
            bootstrap_servers=self.CONFIG["kafka"]["bootstrap_servers"],
        )
        db_connection = asyncpg.connect(
            dsn=self.CONFIG["db"]["dsn"],
        )
        session = ClientSession()
        cron_runner = CronRunner()

        self._periodic_producer = PeriodicProducer(
            kafka_producer_client=kafka_producer_client,
            topic=self.CONFIG["kafka"]["topic"],
            session=session,
            cron_runner=cron_runner,
        )
        self._periodic_consumer = PeriodicConsumer(
            kafka_consumer_client=kafka_consumer_client,
            db_connection=db_connection,
            cron_runner=cron_runner,
        )

    async def start(
            self,
            periodic_checker_inputs: List[PeriodicCheckerInput]
    ) -> None:
        if not periodic_checker_inputs:
            LOGGER.warning("No checks defined, exiting")
            return

        await self._periodic_producer.start(periodic_checker_inputs)
        await self._periodic_consumer.start()
