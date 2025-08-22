"""
Token schema.

This module contains Pydantic models for token responses.
"""

from pydantic import BaseModel

from app.api.schemas.user_schemas import User


class TokenResponse(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
    user: User
    email: str
    role: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""

    refresh_token: str
