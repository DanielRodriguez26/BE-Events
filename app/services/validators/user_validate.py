from app.api.schemas.user_schemas import UserCreate
from app.db.models import User as UserModel

def validate_user(user: UserCreate) -> UserCreate:
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
    
    if not user.role: # type:ignore
        raise ValueError("Role is required")

    #si el user name ya existe, lanzar un error
    if UserModel.query.filter_by(username=user.username).first():
        raise ValueError("Username already exists")
    
    #si el email ya existe, lanzar un error
    if UserModel.query.filter_by(email=user.email).first():
        raise ValueError("Email already exists")
    
    return user




