import json
import logging

from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)


class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    async def start(self) -> None:
        logger.info("Starting Kafka producer...")
        await self._producer.start()

    async def stop(self) -> None:
        logger.info("Stopping Kafka producer...")
        await self._producer.stop()

    async def send(self, topic: str, message: dict) -> None:
        logger.info(f"Sending message to Kafka: topic={topic}, message={message}")
        await self._producer.send_and_wait(topic, message)
