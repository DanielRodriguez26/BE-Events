import math
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.event_schemas import Event, EventCreate, EventUpdate
from app.api.schemas.pagination_schema import Page
from app.core.dependencies import require_admin, require_organizer
from app.db.base import get_db
from app.db.models import User
from app.services.event_service import EventService

router = APIRouter()


@router.get("/", response_model=Page[Event], summary="Get all events")
async def get_all_events(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of events per page"),
    db: Session = Depends(get_db),
    #current_user: User = Depends(require_admin),
):
    """
    Retrieve all events with pagination.

    - **page**: Page number to retrieve (starts at 1)
    - **size**: Number of events per page (max 100)
    """
    try:
        event_service = EventService(db)
        skip = (page - 1) * size
        events = event_service.get_all_events(skip=skip, page=page, limit=size)

        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/search", response_model=List[Event], summary="Search events by multiple criteria")
async def search_events(
    title: Optional[str] = Query(None, description="Search by title or part of title"),
    location: Optional[str] = Query(
        None, description="Search by location or part of location"
    ),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    date_from: Optional[datetime] = Query(
        None, description="Start of date range (ISO format)"
    ),
    date_to: Optional[datetime] = Query(
        None, description="End of date range (ISO format)"
    ),
    skip: int = Query(0, ge=0, description="Number of events to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of events to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Search events by multiple criteria:

    - **title**: Search by title or part of title (case insensitive)
    - **location**: Search by location or part of location (case insensitive)
    - **is_active**: Filter by active status (true/false)
    - **date_from**: Start of date range (events that occur from this date)
    - **date_to**: End of date range (events that occur until this date)
    - **skip**: Number of events to skip (for pagination)
    - **limit**: Maximum number of events to return (max 1000)
    """
    try:
        event_service = EventService(db)
        events = event_service.search_events(
            title=title,
            location=location,
            is_active=is_active,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit,
        )
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
        event_service = EventService(db)
        event = event_service.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/", response_model=Event, summary="Create new event", dependencies=[Depends(require_organizer)])
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    #current_user: User = Depends(require_organizer),
):
    """
    Create a new event.

    **Requires:** Organizer or Admin role

    - **event**: Event data to create
    """
    try:
        event_service = EventService(db)
        new_event = event_service.create_new_event(event)
        return new_event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{event_id}", response_model=Event, summary="Update event by ID")
async def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    #current_user: User = Depends(require_organizer),
):
    """
    Update an existing event.

    **Requires:** Organizer or Admin role

    - **event_id**: The unique identifier of the event to update
    - **event**: Updated event data
    """
    try:
        event_service = EventService(db)
        updated_event = event_service.update_event(event_id, event)
        if not updated_event:
            raise HTTPException(status_code=404, detail="Event not found")
        return updated_event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{event_id}", summary="Delete event by ID", dependencies=[Depends(require_admin)])
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    #current_user: User = Depends(require_admin),
):
    """
    Delete an event permanently.

    **Requires:** Admin role

    - **event_id**: The unique identifier of the event to delete
    """
    try:
        event_service = EventService(db)
        deleted = event_service.delete_event(event_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
