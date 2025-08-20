from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.dtos.event_dto import CreateEventDTO, EventDTO, UpdateEventDTO
from app.application.services.event_service import EventService
from app.infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventsRepository,
)

router = APIRouter(prefix="/events", tags=["Events"])


# --- Dependencia para inyectar el servicio ---
def get_event_service() -> EventService:
    # Aquí es donde la "magia" de la inyección de dependencias sucede.
    # Se crea una instancia del repositorio y se pasa al servicio
    repository = InMemoryEventsRepository()
    return EventService(repository)


@router.get("/", response_model=List[EventDTO], status_code=status.HTTP_200_OK)
def get_all_events(service: EventService = Depends(get_event_service)):
    # Obtiene todos los eventos
    return service.get_all_events()


@router.post("/", response_model=EventDTO, status_code=status.HTTP_201_CREATED)
def create_event(
    event: CreateEventDTO, service: EventService = Depends(get_event_service)
):
    # Crea un nuevo evento.
    return service.create_event(event)
