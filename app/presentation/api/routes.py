from fastapi import APIRouter

from app.presentation.api.v1.event.endpoints import router as event_router
from app.presentation.api.v1.event_template.endpoints import (
    router as event_template_router,
)

api_router = APIRouter()

api_router.include_router(event_router, prefix="/event", tags=["Event"])

api_router.include_router(event_template_router, prefix="/template", tags=["Template"])
