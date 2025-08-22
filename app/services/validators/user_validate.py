from app.api.schemas.user_schemas import UserCreate
from app.db.models import User as UserModel
from app.infrastructure.repositories.user_repository import UserRepository


def validate_user(user: UserCreate, user_repository: UserRepository) -> UserCreate:
    """Validate a user."""
    if not user.username:
        raise ValueError("Username is required")
    if not user.email:
        raise ValueError("Email is required")
    if not user.password:
        raise ValueError("Password is required")
    if not user.first_name:
        raise ValueError("First name is required")
    if not user.last_name:
        raise ValueError("Last name is required")
    if not user.confirm_password:
        raise ValueError("Confirm password is required")
    if user.password != user.confirm_password:
        raise ValueError("Passwords do not match")
    if not user.role_id:
        raise ValueError("Role is required")
    # si el user name ya existe, lanzar un error
    if user_repository.get_user_by_username(user.username):
        raise ValueError("Username already exists")

    # si el email ya existe, lanzar un error
    if user_repository.get_user_by_email(user.email):
        raise ValueError("Email already exists")

    return user
