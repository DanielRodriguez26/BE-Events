"""
Authentication schemas.

This module contains Pydantic models for authentication requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login request model."""

    username: str
    password: str


class UserProfile(BaseModel):
    """User profile model."""

    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    is_active: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
