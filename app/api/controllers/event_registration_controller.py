from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.event_registration_schemas import (
    EventRegistration,
    EventRegistrationCreate,
    EventRegistrationUpdate,
    EventRegistrationWithEvent,
)
from app.api.schemas.pagination_schema import Page
from app.core.dependencies import get_current_user
from app.db.base import get_db
from app.db.models.user_model import User
from app.services.event_registration_service import EventRegistrationService

# Router para endpoints de registro a eventos
router = APIRouter()


@router.post("/", response_model=EventRegistration, summary="Register to an event")
async def register_to_event(
    registration_data: EventRegistrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Registra al usuario autenticado a un evento.

    **Requires:** Usuario autenticado

    **Validations:**
    - El evento debe existir y estar activo
    - El usuario no debe estar ya registrado
    - Debe haber capacidad disponible
    - Máximo 10 participantes por registro

    - **registration_data**: Datos del registro
    """
    try:
        registration_service = EventRegistrationService(db)
        registration = registration_service.register_user_to_event(
            user_id=int(current_user.id), registration_data=registration_data
        )
        return registration
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/user_registrations",
    response_model=Page[EventRegistrationWithEvent],
    summary="Get user's event registrations",
)
async def get_user_registrations(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of registrations per page"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene todos los registros del usuario autenticado.

    **Requires:** Usuario autenticado

    - **page**: Número de página (comienza en 1)
    - **size**: Número de registros por página (máximo 100)
    """
    try:
        registration_service = EventRegistrationService(db)
        skip = (page - 1) * size
        registrations = registration_service.get_user_registrations(
            user_id=int(current_user.id), 
            skip=skip, 
            page=page, 
            limit=size
        ) 
        return registrations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/event/{event_id}",
    response_model=Page[EventRegistration],
    summary="Get all registrations for an event",
)
async def get_event_registrations(
    event_id: int,
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of registrations per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene todos los registros de un evento específico.

    **Requires:** Usuario autenticado (Admin u Organizador para ver todos los registros)

    - **event_id**: ID del evento
    - **page**: Número de página (comienza en 1)
    - **size**: Número de registros por página (máximo 100)
    """
    try:
        # Verificar permisos de admin/organizador
        if current_user.role not in ["admin", "organizer"]:
            raise HTTPException(
                status_code=403, detail="No tienes permisos para ver registros de eventos"
            )
        registration_service = EventRegistrationService(db)
        skip = (page - 1) * size
        registrations = registration_service.get_event_registrations(
            event_id=event_id, skip=skip, page=page, limit=size
        )
        return registrations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/{registration_id}",
    response_model=EventRegistration,
    summary="Get registration by ID",
)
async def get_registration_by_id(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene un registro específico por ID.

    **Requires:** Usuario autenticado (solo puede ver sus propios registros o ser admin/organizador)

    - **registration_id**: ID del registro
    """
    try:
        registration_service = EventRegistrationService(db)
        registration = registration_service.get_registration_by_id(registration_id)

        if not registration:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        # Verificar permisos (solo puede ver sus propios registros o ser admin/organizador)
        if registration.user_id != current_user.id:
            # Verificar si es admin u organizador
            if current_user.role not in ["admin", "organizer"]:
                raise HTTPException(
                    status_code=403, detail="No tienes permisos para ver este registro"
                )

        return registration
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/event/{event_id}/capacity", summary="Get event capacity information")
async def get_event_capacity(event_id: int, db: Session = Depends(get_db)):
    """
    Obtiene información de capacidad de un evento.

    - **event_id**: ID del evento

    Returns:
    - total_capacity: Capacidad total del evento
    - registered_participants: Número de participantes registrados
    - available_capacity: Capacidad disponible
    - is_full: Si el evento está lleno
    """
    try:
        registration_service = EventRegistrationService(db)
        capacity_info = registration_service.get_event_capacity_info(event_id)
        return capacity_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
