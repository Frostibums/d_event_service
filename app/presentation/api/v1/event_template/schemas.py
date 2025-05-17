from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.dto import EventTemplateDTO


class EventTemplateCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: str | None = None

    def to_dto(self) -> EventTemplateDTO:
        return EventTemplateDTO(
            title=self.title,
            description=self.description,
        )


class EventTemplateRead(BaseModel):
    id: UUID
    title: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
