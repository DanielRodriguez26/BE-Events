"""
Authentication service.

This module provides authentication and authorization functionality.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.auth_schemas import LoginRequest
from app.api.schemas.token_schema import TokenResponse
from app.api.schemas.user_schemas import UserCreate
from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.db.models import Role, User
from app.services.user_service import UserService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserService(db)

    def login(self, login_data: LoginRequest) -> TokenResponse:
        """Login user and return access token."""
        # 1. First check if user exists
        user = self.user_repo.get_user_by_username(login_data.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        # 2. Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is deactivated",
            )

        # 3. Verify password
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        # 2. Acceder al rol a través de la relación (sin consulta extra)
        role_name = user.role.name if user.role else "user"  # type:ignore

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username, "role": role_name},
            expires_delta=access_token_expires,
        )

        # 3. Acceder a los atributos directamente (sin .value)
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user_id=user.id,
            user=user,
            email=user.email,
            username=user.username,
            role=role_name,
        )

    def register(self, register_data: UserCreate) -> TokenResponse:
        """Register a user."""
        user = self.user_repo.create_user(register_data)
        return self.login(LoginRequest(username=user.username, password=register_data.password))

    def get_current_user(self, token: str) -> User:
        """Get current user from token."""
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id: str = payload.get("sub")  # type:ignore
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = self.db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
