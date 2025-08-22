from datetime import datetime
import math
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.schemas.event_schemas import Event, EventCreate, EventUpdate
from app.api.schemas.pagination_schema import Page
from app.infrastructure.repositories.event_repository import EventRepository
from app.services.validators.event_validators import (
    validate_event_data,
    validate_event_update_data,
)


class EventService:
    def __init__(self, db: Session):
        self.db = db
        self.event_repository = EventRepository(db)

    def get_all_events(self, skip: int = 0,page: int =1, limit: int = 100) ->Page:
        """Get all events with business logic validation."""
        events = self.event_repository.get_all_events(skip=skip, limit=limit)
        eventList = [Event.from_orm(event) for event in events]
        total_events = self.event_repository.get_events_count()
        total_pages = math.ceil(total_events / limit) if total_events > 0 else 1
        
        return Page(
            items=eventList,
            page=page,
            size=limit,
            total_items=total_events,
            total_pages=total_pages,
        )

    def get_total_events_count(self) -> int:
        """Get the total number of events."""
        return self.event_repository.get_events_count()

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID with business logic validation."""
        event = self.event_repository.get_event(event_id)
        if event:
            return Event.from_orm(event)
        return None

    def create_new_event(self, event_data: EventCreate) -> Event:
        """Create new event with business logic validation."""
        events = self.event_repository.get_all_events()
        # Validate event data
        validate_event_data(event_data, events)

        event = self.event_repository.create_event(event_data)
        return Event.from_orm(event)

    def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Update existing event with business logic validation."""
        current_event = self.event_repository.get_event(event_id)
        if not current_event:
            raise ValueError("Event not found")

        validate_event_update_data(event_data, current_event)

        updated_event = self.event_repository.update_event(event_id, event_data)
        if updated_event:
            return Event.from_orm(updated_event)
        return None

    def delete_event(self, event_id: int) -> bool:
        """Delete existing event with business logic validation."""
        return self.event_repository.delete_event(event_id)

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
