"""
Token schema.

This module contains Pydantic models for token responses.
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
    username: str
    email: str
    role: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""

    refresh_token: str
