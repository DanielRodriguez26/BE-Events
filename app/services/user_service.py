import math
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.schemas.pagination_schema import Page
from app.api.schemas.user_schemas import User, UserCreate
from app.core.security import get_password_hash, verify_password
from app.infrastructure.repositories.user_repository import UserRepository
from app.services.validators.user_validate import validate_user


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_all_users(self, skip: int = 0, page: int = 1, limit: int = 100) -> Page:
        """Get all users with business logic validation."""
        users = self.user_repository.get_all_users(skip=skip, limit=limit)
        userList = [User.model_validate(user) for user in users]
        total_users = self.user_repository.get_users_count()
        total_pages = math.ceil(total_users / limit) if total_users > 0 else 1

        return Page(
            items=userList,
            page=page,
            size=limit,
            total_items=total_users,
            total_pages=total_pages,
        )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID with business logic validation."""
        user = self.user_repository.get_user(user_id)
        if user:
            return User.model_validate(user)
        return None

    def get_user_by_username(self, username: str):
        """Get user by username (returns SQLAlchemy object for internal use)."""
        return self.user_repository.get_user_by_username(username)

    def get_user_by_email(self, email: str):
        """Get user by email (returns SQLAlchemy object for internal use)."""
        return self.user_repository.get_user_by_email(email)

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
