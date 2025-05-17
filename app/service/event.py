from uuid import UUID

from app.domain.dto import EventDTO
from app.domain.entities.event import Event
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repositories.event import EventRepository


class EventService:
    def __init__(self, repository: EventRepository, kafka_producer: KafkaEventProducer):
        self.repository = repository
        self.kafka_producer = kafka_producer

    async def create(self, data: EventDTO) -> Event:
        event = await self.repository.create(data)

        await self.kafka_producer.send(
            topic="event-started",
            message={
                "event_id": str(event.id),
                "group_id": str(event.group_id),
                "template_id": str(event.template.id),
                "start_time": event.start_time.isoformat(),
            },
        )

        return event

    async def get(self, event_id: UUID) -> Event:
        return await self.repository.get(event_id)

    async def get_list(self) -> list[Event]:
        return await self.repository.get_list()
