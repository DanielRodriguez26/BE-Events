from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas import Event, EventCreate
from app.db.base import get_db
from app.services.event_service import EventService

router = APIRouter()


@router.get("/", response_model=List[Event], summary="Get all events")
async def get_all_events(
    skip: int = Query(0, ge=0, description="Number of events to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of events to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve all events with pagination.

    - **skip**: Number of events to skip (for pagination)
    - **limit**: Maximum number of events to return (max 1000)
    """
    try:
        events = EventService.get_all_events(db, skip=skip, limit=limit)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{event_id}", response_model=Event, summary="Get event by ID")
async def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific event by its ID.

    - **event_id**: The unique identifier of the event
    """
    try:
        event = EventService.get_event_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/", response_model=Event, summary="Create new event")
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event.

    - **event**: Event data to create
    """
    try:
        new_event = EventService.create_new_event(db, event)
        return new_event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
