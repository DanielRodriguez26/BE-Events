from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.auth_schemas import LoginRequest
from app.api.schemas.token_schema import TokenResponse
from app.api.schemas.user_schemas import UserCreate
from app.db.base import get_db
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Login a user")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login a user."""
    auth_service = AuthService(db)
    return auth_service.login(login_data)


@router.post("/register", response_model=TokenResponse, summary="Register a user")
async def register(register_data: UserCreate, db: Session = Depends(get_db)):
    """Register a user."""
    auth_service = AuthService(db)
    return auth_service.register(register_data)
