import math
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session as DBSession

from app.api.schemas.event_schemas import (
    Event,
    EventCreate,
    EventUpdate,
    EventWithCapacity,
)
from app.api.schemas.pagination_schema import Page
from app.api.schemas.session_schemas import Session as SessionSchema
from app.api.schemas.session_schemas import SessionCreate, SessionCreateForEvent
from app.core.dependencies import get_current_user, require_admin, require_organizer
from app.core.exceptions import (
    NotFoundException,
    ServerException,
    ValidationException,
    create_validation_error,
)
from app.db.base import get_db
from app.db.models import User
from app.services.event_service import EventService

router = APIRouter()


@router.get("/", response_model=Page[Event], summary="Get all events")
async def get_all_events(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of events per page"),
    db: DBSession = Depends(get_db),
    # current_user: User = Depends(require_admin),
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


@router.get(
    "/search", response_model=Page[Event], summary="Search events by multiple criteria"
)
async def search_events(
    title: Optional[str] = Query(None, description="Search by title or part of title"),
    location: Optional[str] = Query(
        None, description="Search by location or part of location"
    ),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    date_from: Optional[str] = Query(
        None, description="Start of date range (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
    ),
    date_to: Optional[str] = Query(
        None, description="End of date range (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of events per page"),
    db: DBSession = Depends(get_db),
):
    """
    Search events by multiple criteria:

    - **title**: Search by title or part of title (case insensitive)
    - **location**: Search by location or part of location (case insensitive)
    - **is_active**: Filter by active status (true/false)
    - **date_from**: Start of date range (events that occur from this date) - YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
    - **date_to**: End of date range (events that occur until this date) - YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
    - **page**: Page number (starts at 1)
    - **size**: Number of events per page (max 100)
    """
    try:
        # Convert date strings to datetime objects
        parsed_date_from = None
        parsed_date_to = None

        if date_from and date_from.strip():
            try:
                parsed_date_from = datetime.fromisoformat(
                    date_from.replace("Z", "+00:00")
                )
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date_from format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS",
                )

        if date_to and date_to.strip():
            try:
                parsed_date_to = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date_to format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS",
                )

        # Calculate skip based on page and size
        skip = (page - 1) * size

        event_service = EventService(db)
        events = event_service.search_events(
            title=title,
            location=location,
            is_active=is_active,
            date_from=parsed_date_from,
            date_to=parsed_date_to,
            page=page,
            skip=skip,
            limit=size,
        )
        return events
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{event_id}", response_model=Event, summary="Get event by ID")
async def get_event_by_id(
    event_id: int, db: DBSession = Depends(get_db), request: Request = None
):
    """
    Retrieve a specific event by its ID.

    - **event_id**: The unique identifier of the event
    """
    try:
        event_service = EventService(db)
        event = event_service.get_event_by_id(event_id)
        if not event:
            raise NotFoundException(
                message="Evento no encontrado",
                path=str(request.url.path) if request else None,
                method=request.method if request else None,
            )
        return event
    except (NotFoundException, ValidationException, ServerException):
        raise
    except Exception as e:
        raise ServerException(
            message=f"Error interno del servidor: {str(e)}",
            path=str(request.url.path) if request else None,
            method=request.method if request else None,
        )


@router.get(
    "/upcoming/with-capacity",
    response_model=Page[EventWithCapacity],
    summary="Get upcoming events with capacity info",
)
async def get_upcoming_events_with_capacity(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of events per page"),
    db: DBSession = Depends(get_db),
):
    """
    Retrieve upcoming events with capacity information and pagination.

    Returns events that:
    - Are active
    - Have a future date
    - Include capacity information

    - **page**: Page number to retrieve (starts at 1)
    - **size**: Number of events per page (max 100)
    """
    try:
        event_service = EventService(db)
        skip = (page - 1) * size
        events = event_service.get_upcoming_events_with_capacity(
            skip=skip, page=page, limit=size
        )
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/with-capacity",
    response_model=Page[EventWithCapacity],
    summary="Get all events with capacity info",
)
async def get_all_events_with_capacity(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of events per page"),
    db: DBSession = Depends(get_db),
):
    """
    Retrieve all events with capacity information and pagination.

    Returns events that:
    - Are active
    - Include capacity information

    - **page**: Page number to retrieve (starts at 1)
    - **size**: Number of events per page (max 100)
    """
    try:
        event_service = EventService(db)
        skip = (page - 1) * size
        events = event_service.get_all_events_with_capacity(
            skip=skip, page=page, limit=size
        )
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/", response_model=Event, summary="Create new event")
async def create_event(
    event: EventCreate,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.delete("/{event_id}", summary="Delete event by ID")
async def delete_event(
    event_id: int,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


# Session endpoints for events
@router.get(
    "/{event_id}/sessions",
    response_model=Page[SessionSchema],
    summary="Get sessions by event",
)
async def get_event_sessions(
    event_id: int,
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of sessions per page"),
    db: DBSession = Depends(get_db),
):
    """
    Retrieve all sessions for a specific event with pagination.

    - **event_id**: The unique identifier of the event
    - **page**: Page number to retrieve (starts at 1)
    - **size**: Number of sessions per page (max 100)
    """
    try:
        from app.services.session_service import SessionService

        session_service = SessionService(db)
        skip = (page - 1) * size
        sessions = session_service.get_sessions_by_event(
            event_id, skip=skip, page=page, limit=size
        )
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/{event_id}/sessions",
    response_model=SessionSchema,
    summary="Create session for event",
)
async def create_event_session(
    event_id: int,
    session: SessionCreateForEvent,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(require_organizer),
):
    """
    Create a new session for a specific event.

    **Requires:** Organizer or Admin role

    **Validations:**
    - Session schedule must be within the event's date range
    - No schedule conflicts with existing sessions
    - Speaker must exist (if provided)
    - Capacity must be positive (if provided)

    - **event_id**: The unique identifier of the event
    - **session**: Session data to create
    """
    try:
        from app.api.schemas.session_schemas import SessionCreate
        from app.services.session_service import SessionService

        # Override event_id to ensure it matches the URL parameter
        session_data = session.model_dump()
        session_data["event_id"] = event_id

        session_service = SessionService(db)
        new_session = session_service.create_session(SessionCreate(**session_data))
        return new_session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
