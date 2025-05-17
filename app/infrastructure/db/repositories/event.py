from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dto import EventDTO
from app.domain.entities.event import Event
from app.infrastructure.db.models.event import EventORM


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, object_id: UUID) -> Event | None:
        result = await self.session.execute(
            select(EventORM).where(EventORM.id == object_id)
        )
        event = result.scalar_one_or_none()
        return event.to_domain() if event else None

    async def create(self, event: EventDTO) -> Event:
        orm = EventORM(**event.__dict__)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return orm.to_domain()

    async def get_list(self) -> list[Event]:
        result = await self.session.execute(
            select(EventORM)
        )
        orm = result.scalars()
        return [event.to_domain() for event in orm]
