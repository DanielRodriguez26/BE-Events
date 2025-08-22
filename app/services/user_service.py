from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.schemas.user_schemas import User, UserCreate
from app.core.security import get_password_hash, verify_password
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.validators.user_validate import validate_user


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with business logic validation."""
        users = self.user_repository.get_all_users(skip=skip, limit=limit)
        return [User.from_orm(user) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID with business logic validation."""
        user = self.user_repository.get_user(user_id)
        if user:
            return User.from_orm(user)
        return None

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Login a user."""
        if not username or not password:
            return None
        if not username.strip() or not password.strip():
            return None

        user = self.user_repository.get_user_by_username(username)

        if not user:
            return None

        if not verify_password(password, user.password):  # type:ignore
            return None

        # Return user even if inactive - let AuthService handle the active check
        return user

    def create_user(self, user_data: UserCreate) -> User:
        """Create a user."""
        user_data = validate_user(user_data, self.user_repository)
        
        user_data.password = get_password_hash(user_data.password)

        return self.user_repository.create_user(user_data)