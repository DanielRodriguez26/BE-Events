from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Form,HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.user_schemas import User
from app.db.base import get_db
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[User], summary="Get all users")
async def get_all_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of users to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve all users with pagination.

    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of events to return (max 1000)
    """
    try:
        user_service = UserService(db)
        users = user_service.get_all_users(skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    



