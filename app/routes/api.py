"""
Módulo de rutas de la API.

Este módulo centraliza todas las rutas de la API y su configuración.
"""

from fastapi import APIRouter

from app.api.controllers.auth_controller import router as auth_router
from app.api.controllers.event_registration_controller import (
    router as event_registration_router,
)
from app.api.controllers.events_controller import router as events_router
from app.api.controllers.session_controler import router as sessions_router
from app.api.controllers.speakers_controller import router as speakers_router
from app.api.controllers.user_controller import router as user_router

# Crear router principal de la API
api_router = APIRouter()

# Incluir todos los módulos de rutas
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(speakers_router, prefix="/speakers", tags=["Speakers"])
api_router.include_router(sessions_router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(event_registration_router, prefix="/event-registrations",tags=["Event Registrations"])