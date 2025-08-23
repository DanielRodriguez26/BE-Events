from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.auth_schemas import LoginRequest
from app.api.schemas.token_schema import TokenResponse
from app.api.schemas.user_schemas import UserCreate
from app.core.dependencies import get_current_user
from app.db.base import get_db
from app.db.models import User
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Login a user")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login a user."""
    try:
        auth_service = AuthService(db)
        return auth_service.login(login_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e


@router.post("/register", response_model=TokenResponse, summary="Register a user")
async def register(register_data: UserCreate, db: Session = Depends(get_db)):
    """Register a user."""
    try:
        auth_service = AuthService(db)
        return auth_service.register(register_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/me", summary="Get current user info")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current authenticated user information."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.name if current_user.role else "user",
        "is_active": current_user.is_active,
    }
