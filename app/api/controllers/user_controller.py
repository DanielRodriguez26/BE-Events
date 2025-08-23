from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.user_schemas import User, UserUpdate
from app.core.dependencies import get_current_user, require_admin
from app.db.base import get_db
from app.db.models import User as UserModel
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[User], summary="Get all users")
async def get_all_users(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    size: int = Query(20, ge=1, le=100, description="Number of events per page"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_admin),
):
    """
    Retrieve all users with pagination.

    **Requires:** Admin role

    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return (max 1000)
    """
    try:
        user_service = UserService(db)
        skip = (page - 1) * size
        users = user_service.get_all_users(skip=skip, page=page, limit=size)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/me", response_model=User, summary="Get current user profile")
async def get_current_user_profile(current_user: UserModel = Depends(get_current_user)):
    """
    Obtiene el perfil del usuario autenticado.

    **Requires:** Usuario autenticado
    """
    return current_user


@router.put("/me", response_model=User, summary="Update current user profile")
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza el perfil del usuario autenticado.

    **Requires:** Usuario autenticado

    - **user_update**: Datos a actualizar (name, email, etc.)
    """
    try:
        user_service = UserService(db)
        # Convertir el esquema a diccionario, excluyendo valores None
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        updated_user = user_service.update_user(current_user.id, update_data)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
