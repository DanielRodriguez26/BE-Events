from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    start_date: datetime
    end_date: datetime
    capacity: int = 0
    is_active: bool = True


class EventCreate(EventBase):
    id: Optional[int] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
