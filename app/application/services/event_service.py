import uuid
from typing import List

from app.application.dtos.event_dto import CreateEventDTO, EventDTO, UpdateEventDTO
from app.domain.entities.events import Event
from app.domain.repositories.events_repository import IEventsRepository
from datetime import datetime, timezone


class EventService:
    def __init__(self, repository: IEventsRepository):
        self._repository = repository

    def get_all_events(self) -> List[EventDTO]:
        events = self._repository.get_all_events()
        return [EventDTO.model_validate(event) for event in events]

    def get_event_by_id(self, event_id: uuid.UUID) -> EventDTO:
        event = self._repository.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        return EventDTO.model_validate(event)

    def create_event(self, event_dto: CreateEventDTO) -> EventDTO:
        event_data = event_dto.model_dump()
        now = datetime.now(timezone.utc)
        event = Event(**event_data, created_at=now, updated_at=now)
        created_event = self._repository.create_event(event)
        return EventDTO.model_validate(created_event)

    def update_event(self, event_id: uuid.UUID, event_dto: UpdateEventDTO) -> EventDTO:
        event_data = event_dto.model_dump(exclude_unset=True)
        existing = self._repository.get_event_by_id(event_id)
        if not existing:
            raise ValueError("Event not found")
        merged = existing.model_copy(update={**event_data, "updated_at": datetime.now(timezone.utc)})
        updated_event = self._repository.update_event(merged)
        return EventDTO.model_validate(updated_event)

    def delete_event(self, event_id: uuid.UUID) -> None:
        existing = self._repository.get_event_by_id(event_id)
        if not existing:
            raise ValueError("Event not found")
        self._repository.delete_event(event_id)
