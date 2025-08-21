from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.schemas.event_schemas import Event, EventCreate, EventUpdate
from app.crud.crud_event import EventRepository
class EventService:
    def __init__(self, db: Session):
        self.db = db
        self.event_repository = EventRepository(db)

    @staticmethod
    def get_all_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Get all events with business logic validation."""
        events = self.event_repository.get_all_events(skip=skip, limit=limit)
        return [Event.from_orm(event) for event in events]

    @staticmethod
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID with business logic validation."""
        event = self.event_repository.get_event(event_id)
        if event:
            return Event.from_orm(event)
        return None

    @staticmethod
    def create_new_event(self, event_data: EventCreate) -> Event:
        """Create new event with business logic validation."""
        # Validate that end_date is after start_date
        if event_data.end_date <= event_data.start_date:
            raise ValueError("End date must be after start date")

        # Validate capacity is positive
        if event_data.capacity < 0:
            raise ValueError("Capacity must be a positive number")

        event = self.event_repository.create_event(event_data)
        return Event.from_orm(event)

    @staticmethod
    def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Update existing event with business logic validation."""
        # Get current event
        current_event = self.event_repository.get_event(event_id)
        if not current_event:
            return None

        # Validate dates if provided
        if event_data.start_date and event_data.end_date:
            if event_data.end_date <= event_data.start_date:
                raise ValueError("End date must be after start date")

        # Validate capacity if provided
        if event_data.capacity is not None and event_data.capacity < 0:
            raise ValueError("Capacity must be a positive number")

        updated_event = self.event_repository.update_event(event_id, event_data)
        if updated_event:
            return Event.from_orm(updated_event)
        return None

    @staticmethod
    def delete_event(self, event_id: int) -> bool:
        """Delete existing event with business logic validation."""
        return self.event_repository.delete_event(event_id)

    @staticmethod
    def search_events( 
        self,
        title: Optional[str] = None,
        location: Optional[str] = None,
        is_active: Optional[bool] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Event]:
        """Search events by multiple criteria with business logic validation."""

        events = self.event_repository.search_events(
            title=title,
            location=location,
            is_active=is_active,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit,
        )
        return [Event.from_orm(event) for event in events]
