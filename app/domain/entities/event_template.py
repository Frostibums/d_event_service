from dataclasses import dataclass
from uuid import UUID


@dataclass
class EventTemplate:
    id: UUID
    title: str
    description: str | None
