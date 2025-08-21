"""
API routes module.

This module centralizes all API routes and their configuration.
"""

from fastapi import APIRouter

from app.api.controllers.auth_controller import router as auth_router
from app.api.controllers.events_controller import router as events_router
from app.api.controllers.user_controller import router as user_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
