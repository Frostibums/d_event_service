from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.presentation.api.v1.dependencies import (
    get_current_teacher_id,
    get_event_service,
)
from app.presentation.api.v1.event.schemas import EventCreate, EventRead
from app.service.event import EventService

router = APIRouter()


@router.get("", response_model=list[EventRead], status_code=status.HTTP_200_OK)
async def get_events(
    service: EventService = Depends(get_event_service),
):
    return await service.get_list()


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    data: EventCreate,
    user_id: UUID = Depends(get_current_teacher_id),
    service: EventService = Depends(get_event_service),
):
    if not data.owner_id:
        data.owner_id = user_id
    return await service.create(data.to_dto())


@router.get("/{event_id}", response_model=EventRead, status_code=status.HTTP_200_OK)
async def get_event(
    event_id: UUID,
    service: EventService = Depends(get_event_service),
):
    return await service.get(event_id)
