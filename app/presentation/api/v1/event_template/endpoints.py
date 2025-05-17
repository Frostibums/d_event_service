from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.presentation.api.v1.dependencies import (
    get_event_template_service,
)
from app.presentation.api.v1.event_template.schemas import (
    EventTemplateCreate,
    EventTemplateRead,
)
from app.service.event_template import EventTemplateService

router = APIRouter()


@router.get("", response_model=list[EventTemplateRead])
async def get_event_templates(
    name: str | None = None,
    service: EventTemplateService = Depends(get_event_template_service),
):
    return await service.get_list(name=name)


@router.post("", response_model=EventTemplateRead, status_code=status.HTTP_201_CREATED)
async def create_event_template(
    data: EventTemplateCreate,
    service: EventTemplateService = Depends(get_event_template_service),
):
    try:
        return await service.create(data.to_dto())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{template_id}", response_model=EventTemplateRead)
async def get_event_template(
    template_id: UUID,
    service: EventTemplateService = Depends(get_event_template_service),
):
    return await service.get(template_id)
