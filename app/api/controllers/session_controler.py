import math
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as DBSession

from app.api.schemas.pagination_schema import Page
from app.api.schemas.session_schemas import Session as SessionSchema
from app.api.schemas.session_schemas import SessionCreate, SessionUpdate
from app.db.base import get_db
from app.services.session_service import SessionService

router = APIRouter()


@router.get("/", response_model=Page[SessionSchema], summary="Get all sessions")
async def get_all_sessions(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of sessions per page"),
    db: DBSession = Depends(get_db),
):
    """
    Retrieve all sessions with pagination.

    - **page**: Page number to retrieve (starts at 1)
    - **size**: Number of sessions per page (max 100)
    """
    try:
        session_service = SessionService(db)
        skip = (page - 1) * size
        sessions = session_service.get_all_sessions(skip=skip, page=page, limit=size)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/event/{event_id}",
    response_model=Page[SessionSchema],
    summary="Get sessions by event",
)
async def get_sessions_by_event(
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
        session_service = SessionService(db)
        skip = (page - 1) * size
        sessions = session_service.get_sessions_by_event(
            event_id, skip=skip, page=page, limit=size
        )
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{session_id}", response_model=SessionSchema, summary="Get session by ID")
async def get_session_by_id(session_id: int, db: DBSession = Depends(get_db)):
    """
    Retrieve a specific session by its ID.

    - **session_id**: The unique identifier of the session
    """
    try:
        session_service = SessionService(db)
        session = session_service.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/", response_model=SessionSchema, summary="Create new session")
async def create_session(session: SessionCreate, db: DBSession = Depends(get_db)):
    """
    Create a new session.

    **Validations:**
    - Session schedule must be within the event's date range
    - No schedule conflicts with existing sessions
    - Speaker must exist (if provided)
    - Capacity must be positive (if provided)
    """
    try:
        session_service = SessionService(db)
        new_session = session_service.create_session(session)
        return new_session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put(
    "/{session_id}", response_model=SessionSchema, summary="Update session by ID"
)
async def update_session(
    session_id: int, session: SessionUpdate, db: DBSession = Depends(get_db)
):
    """
    Update an existing session.

    **Validations:**
    - Session schedule must be within the event's date range
    - No schedule conflicts with existing sessions
    - Speaker must exist (if provided)
    - Capacity must be positive (if provided)

    - **session_id**: The unique identifier of the session to update
    - **session**: Updated session data
    """
    try:
        session_service = SessionService(db)
        updated_session = session_service.update_session(session_id, session)
        if not updated_session:
            raise HTTPException(status_code=404, detail="Session not found")
        return updated_session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{session_id}", summary="Delete session by ID")
async def delete_session(session_id: int, db: DBSession = Depends(get_db)):
    """
    Delete a session permanently.

    - **session_id**: The unique identifier of the session to delete
    """
    try:
        session_service = SessionService(db)
        deleted = session_service.delete_session(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
