import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.event_template import EventTemplate
from app.infrastructure.db.session import Base


class EventTemplateORM(Base):
    __tablename__ = "event_templates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    events: Mapped[list["EventORM"]] = relationship(  # noqa: F821
        "EventORM",
        back_populates="template",
    )

    def to_domain(self) -> EventTemplate:
        return EventTemplate(
            id=self.id,
            title=self.title,
            description=self.description,
        )

    @classmethod
    def from_domain(cls, template: EventTemplate) -> "EventTemplateORM":
        return cls(
            id=template.id,
            title=template.title,
            description=template.description,
        )
