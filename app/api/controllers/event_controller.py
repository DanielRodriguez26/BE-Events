from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException

from app.application.dtos.event_dto import CreateEventDTO, EventDTO, UpdateEventDTO
from app.application.services.event_service import EventService
import os
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventsRepository
from app.infrastructure.repositories.sqlalchemy_event_repository import SQLAlchemyEventsRepository

router = APIRouter(prefix="/events", tags=["Events"])


# --- Dependencia para inyectar el servicio ---
def get_event_service() -> EventService:
    backend = os.getenv("REPO_BACKEND", "memory").lower()
    if backend == "sql":
        repository = SQLAlchemyEventsRepository()
    else:
        repository = InMemoryEventsRepository()
    return EventService(repository)


@router.get("/", response_model=List[EventDTO], status_code=status.HTTP_200_OK)
def get_all_events(service: EventService = Depends(get_event_service)):
    return service.get_all_events()


@router.post("/", response_model=EventDTO, status_code=status.HTTP_201_CREATED)
def create_event(event: CreateEventDTO, service: EventService = Depends(get_event_service)):
    return service.create_event(event)


@router.get("/{event_id}", response_model=EventDTO, status_code=status.HTTP_200_OK)
def get_event_by_id(event_id: UUID, service: EventService = Depends(get_event_service)):
    try:
        return service.get_event_by_id(event_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@router.put("/{event_id}", response_model=EventDTO, status_code=status.HTTP_200_OK)
def update_event(event_id: UUID, event: UpdateEventDTO, service: EventService = Depends(get_event_service)):
    try:
        return service.update_event(event_id, event)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: UUID, service: EventService = Depends(get_event_service)):
    try:
        service.delete_event(event_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
