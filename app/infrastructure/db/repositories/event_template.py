from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dto import EventTemplateDTO
from app.domain.entities.event_template import EventTemplate
from app.infrastructure.db.models.event_template import EventTemplateORM


class EventTemplateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, object_id: UUID) -> EventTemplate | None:
        result = await self.session.execute(
            select(EventTemplateORM).where(EventTemplateORM.id == object_id)
        )
        orm = result.scalar_one_or_none()
        return orm.to_domain() if orm else None

    async def create(self, template: EventTemplateDTO) -> EventTemplate:
        orm = EventTemplateORM(**template.__dict__)
        try:
            self.session.add(orm)
            await self.session.commit()
        except IntegrityError as e:
            raise ValueError("Event with such title already exists") from e
        await self.session.refresh(orm)
        return orm.to_domain()

    async def get_list(self, title_filter: str | None = None) -> list[EventTemplate]:
        query = select(EventTemplateORM)
        if title_filter:
            query = query.where(EventTemplateORM.title.ilike(f"%{title_filter}%"))
        result = await self.session.scalars(query)
        return [event.to_domain() for event in result]
