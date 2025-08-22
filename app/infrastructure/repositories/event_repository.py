from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.api.schemas.event_schemas import EventCreate, EventUpdate
from app.db.models import Event


class EventRepository:
    def __init__(self, db: Session):
        self.db = db
        self.event_model = Event

    def get_event(self, event_id: int) -> Optional[Event]:
        """Get a single event by ID."""
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_all_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Get all events with pagination."""
        return self.db.query(Event).offset(skip).limit(limit).all()

    def get_events_count(self) -> int:
        """Get the total number of events."""
        return self.db.query(func.count(self.event_model.id)).scalar() or 0

    def create_event(self, event: EventCreate) -> Event:
        """Create a new event."""
        db_event = Event(**event.dict())
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def update_event(self, event_id: int, event: EventUpdate) -> Optional[Event]:
        """Update an existing event."""
        db_event = self.get_event(event_id)
        if db_event:
            update_data = event.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_event, field, value)
            self.db.commit()
            self.db.refresh(db_event)
        return db_event

    def delete_event(self, event_id: int) -> bool:
        """Delete an event."""
        db_event = self.get_event(event_id)
        if db_event:
            self.db.delete(db_event)
            self.db.commit()
            return True
        return False

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
        """
        Search events by multiple criteria:
        - title: search by title or part of title (case insensitive)
        - location: search by location (case insensitive)
        - is_active: filter by active status
        - date_from/date_to: filter events that occur within this date range
        """
        query = self.db.query(Event)

        # Filter by title (case insensitive partial match)
        if title:
            query = query.filter(Event.title.ilike(f"%{title}%"))

        # Filter by location (case insensitive partial match)
        if location:
            query = query.filter(
                func.lower(Event.location).contains(func.lower(location))
            )

        # Filter by active status
        if is_active is not None:
            query = query.filter(Event.is_active == is_active)

        # Filter by date range (events that overlap with the given period)
        if date_from and date_to:
            # Events that start before the end of the range AND end after the start of the range
            query = query.filter(
                and_(Event.start_date <= date_to, Event.end_date >= date_from)
            )
        elif date_from:
            # Events that end after the start date
            query = query.filter(Event.end_date >= date_from)
        elif date_to:
            # Events that start before the end date
            query = query.filter(Event.start_date <= date_to)

        # Apply pagination
        return query.offset(skip).limit(limit).all()
