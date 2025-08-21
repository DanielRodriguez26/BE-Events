import uuid
from typing import List, Optional
from app.domain.entities.events import Event
from app.domain.repositories.events_repository import IEventsRepository

class InMemoryEventsRepository(IEventsRepository):
    _shared_events: List[Event] = []

    def __init__(self):
        # Compartir almacenamiento entre instancias para que los endpoints vean el mismo estado
        self._events: List[Event] = InMemoryEventsRepository._shared_events

    def get_all_events(self) -> List[Event]:
        return self._events

    def get_event_by_id(self, event_id: uuid.UUID) -> Optional[Event]:
        for event in self._events:
            if event.id == event_id:
                return event
        return None

    def create_event(self, event: Event) -> Event:
        self._events.append(event)
        return event

    def update_event(self, event: Event) -> Event:
        for idx, existing_event in enumerate(self._events):
            if existing_event.id == event.id:
                self._events[idx] = event
                return event
        raise ValueError("Event not found")

    def delete_event(self, event_id: uuid.UUID) -> None:
        self._events = [event for event in self._events if event.id != event_id]