from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone: str
    role_id: int
    is_active: bool = True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    id: Optional[int] = None
    confirm_password: str 


class UserUpdate(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
