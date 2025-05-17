import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.event import Event
from app.domain.entities.event_template import EventTemplate
from app.infrastructure.db.models.event_template import EventTemplateORM
from app.infrastructure.db.session import Base


class EventORM(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    template_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("event_templates.id"),
        nullable=False,
    )
    group_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    template: Mapped[EventTemplateORM | None] = relationship(
        "EventTemplateORM",
        back_populates="events",
        lazy="joined",
    )

    def to_domain(self) -> Event:
        return Event(
            id=self.id,
            owner_id=self.owner_id,
            template=EventTemplate(
                id=self.template.id,
                title=self.template.title,
                description=self.template.description,
            ),
            group_id=self.group_id,
            start_time=self.start_time,
        )

    @classmethod
    def from_domain(cls, event: Event) -> "EventORM":
        return cls(
            id=event.id,
            owner_id=event.owner_id,
            template_id=event.template.id,
            group_id=event.group_id,
            start_time=event.start_time,
        )
