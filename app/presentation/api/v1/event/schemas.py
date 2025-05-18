from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.dto import EventDTO
from app.domain.entities.event_template import EventTemplate


class EventCreate(BaseModel):
    owner_id: UUID | None = None
    template_id: UUID
    group_id: UUID
    start_time: datetime

    def to_dto(self) -> EventDTO:
        return EventDTO(
            owner_id=self.owner_id,
            template_id=self.template_id,
            group_id=self.group_id,
            start_time=self.start_time.utcnow(),
        )


class EventRead(BaseModel):
    id: UUID
    owner_id: UUID
    template: EventTemplate
    group_id: UUID
    start_time: datetime

    model_config = ConfigDict(from_attributes=True)

