from uuid import UUID

from app.domain.dto import EventTemplateDTO
from app.domain.entities.event_template import EventTemplate
from app.infrastructure.db.repositories.event_template import EventTemplateRepository


class EventTemplateService:
    def __init__(self, repository: EventTemplateRepository):
        self.repository = repository

    async def create(self, data: EventTemplateDTO) -> EventTemplate:
        return await self.repository.create(data)

    async def get(self, template_id: UUID) -> EventTemplate:
        return await self.repository.get(template_id)

    async def get_list(self, name: str | None = None) -> list[EventTemplate]:
        return await self.repository.get_list(title_filter=name)
