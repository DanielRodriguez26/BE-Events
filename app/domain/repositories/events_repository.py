from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from app.domain.entities.events import Event

class IEventsRepository(ABC):
    @abstractmethod
    def get_all_events(self) -> List[Event]:
        """Retrieve all events."""
        pass

    @abstractmethod
    def get_event_by_id(self, event_id: uuid.UUID) -> Optional[Event]:
        """Retrieve an event by its ID."""
        pass

    @abstractmethod
    def create_event(self, event: Event) -> Event:
        """Create a new event."""
        pass

    @abstractmethod
    def update_event(self, event: Event) -> Event:
        """Update an existing event."""
        pass

    @abstractmethod
    def delete_event(self, event_id: uuid.UUID) -> None:
        """Delete an event by its ID."""
        pass