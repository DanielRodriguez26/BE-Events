
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Event
from app.api.schemas import EventCreate, EventUpdate


def get_event(db: Session, event_id: int) -> Optional[Event]:
    """Get a single event by ID."""
    return db.query(Event).filter(Event.id == event_id).first()


def get_all_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    """Get all events with pagination."""
    return db.query(Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: EventCreate) -> Event:
    """Create a new event."""
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: int, event: EventUpdate) -> Optional[Event]:
    """Update an existing event."""
    db_event = get_event(db, event_id)
    if db_event:
        update_data = event.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> bool:
    """Delete an event."""
    db_event = get_event(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False
