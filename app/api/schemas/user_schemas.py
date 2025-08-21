from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserCreate(UserBase):
    id: Optional[int] = None


class UserUpdate(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
