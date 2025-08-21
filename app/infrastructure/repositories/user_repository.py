from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.api.schemas.user_schemas import UserCreate, UserUpdate
from app.db.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.user_model = User
    
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get a single user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Login a user."""
        return self.db.query(User).filter(User.username == username, User.password == password).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a user."""
        user = User(**user_data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
