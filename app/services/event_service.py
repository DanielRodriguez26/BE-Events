from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud.crud_event import get_all_events, get_event, create_event, update_event, delete_event
from app.api.schemas import EventCreate, EventUpdate, Event
from datetime import datetime


class EventService:
    @staticmethod
    def get_all_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
        """Get all events with business logic validation."""
        events = get_all_events(db, skip=skip, limit=limit)
        return [Event.from_orm(event) for event in events]

    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
        """Get event by ID with business logic validation."""
        event = get_event(db, event_id)
        if event:
            return Event.from_orm(event)
        return None

    @staticmethod
    def create_new_event(db: Session, event_data: EventCreate) -> Event:
        """Create new event with business logic validation."""
        # Validate that end_date is after start_date
        if event_data.end_date <= event_data.start_date:
            raise ValueError("End date must be after start date")
        
        # Validate capacity is positive
        if event_data.capacity < 0:
            raise ValueError("Capacity must be a positive number")
        
        event = create_event(db, event_data)
        return Event.from_orm(event)

    @staticmethod
    def update_existing_event(db: Session, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Update existing event with business logic validation."""
        # Get current event
        current_event = get_event(db, event_id)
        if not current_event:
            return None
        
        # Validate dates if provided
        if event_data.start_date and event_data.end_date:
            if event_data.end_date <= event_data.start_date:
                raise ValueError("End date must be after start date")
        
        # Validate capacity if provided
        if event_data.capacity is not None and event_data.capacity < 0:
            raise ValueError("Capacity must be a positive number")
        
        updated_event = update_event(db, event_id, event_data)
        if updated_event:
            return Event.from_orm(updated_event)
        return None

    @staticmethod
    def delete_existing_event(db: Session, event_id: int) -> bool:
        """Delete existing event with business logic validation."""
        return delete_event(db, event_id)

