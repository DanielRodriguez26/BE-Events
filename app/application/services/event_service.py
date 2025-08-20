import uuid
from typing import List
from app.domain.entities.events import Event
from app.domain.repositories.events_repository import IEventsRepository
from app.application.dtos.envet_dto import EventDTO


class EventService:
    def __init__(self, repository: IEventsRepository):
        self._repository = repository

    def get_all_events(self) -> List[EventDTO]:
        events = self._repository.get_all_events()
        return [EventDTO.from_orm(event) for event in events]

    def get_event_by_id(self, event_id: uuid.UUID) -> EventDTO:
        event = self._repository.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        return EventDTO.from_orm(event)

    def create_event(self, event_dto: EventDTO) -> EventDTO:
        event = Event(**event_dto.dict())
        created_event = self._repository.create_event(event)
        return EventDTO.from_orm(created_event)

    def update_event(self, event_dto: EventDTO) -> EventDTO:
        event = Event(**event_dto.dict())
        updated_event = self._repository.update_event(event)
        return EventDTO.from_orm(updated_event)

    def delete_event(self, event_id: uuid.UUID) -> None:
        self._repository.delete_event(event_id)