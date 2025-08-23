"""
Dependencies module.

This module contains FastAPI dependencies for authentication and authorization.
"""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db.models import Role, User
from app.services.auth_service import AuthService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user."""
    try:
        auth_service = AuthService(db)
        return auth_service.get_current_user(credentials.credentials)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def require_roles(required_roles: List[str]):
    """Dependency to require specific roles."""

    def role_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
    ) -> User:
        # Get user role
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        if not role or role.name not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(required_roles)}",
            )
        return current_user

    return role_checker


def require_admin(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> User:
    """Require admin role."""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required.",
        )
    return current_user


def require_organizer(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> User:
    """Require organizer role."""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or role.name not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Organizer role required.",
        )
    return current_user


def require_moderator(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
) -> User:
    """Require moderator role."""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or role.name not in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Moderator role required.",
        )
    return current_user


def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Optional authentication - returns user if authenticated, None otherwise."""
    if not credentials:
        return None

    try:
        auth_service = AuthService(db)
        return auth_service.get_current_user(credentials.credentials)
    except HTTPException:
        return None
