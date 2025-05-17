from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.domain.enums.role import Role
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repositories.event import EventRepository
from app.infrastructure.db.repositories.event_template import EventTemplateRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.event import EventService
from app.service.event_template import EventTemplateService


def get_kafka_producer(request: Request) -> KafkaEventProducer:
    return request.app.state.kafka_producer


def get_event_template_service(
        session: AsyncSession = Depends(get_session),
) -> EventTemplateService:
    return EventTemplateService(EventTemplateRepository(session))


def get_event_service(
        session: AsyncSession = Depends(get_session),
        producer: KafkaEventProducer = Depends(get_kafka_producer)
) -> EventService:
    return EventService(
        EventRepository(session),
        producer,
    )


security = HTTPBearer()


def get_jwt_payload(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    if token.startswith("Bearer "):
        token = token[7:]
    try:
        return decode_jwt_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_teacher_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    if payload.get("role") not in (Role.teacher, Role.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for stuff"
        )
    return UUID(payload["sub"])


def get_current_user_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    return UUID(payload["sub"])
