from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.event_template import EventTemplate


@dataclass
class Event:
    id: UUID
    owner_id: UUID
    template: EventTemplate
    group_id: UUID
    start_time: datetime
