from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Session(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    event_id: int
    speaker_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    capacity: Optional[int] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    event_id: int = Field(..., gt=0)
    speaker_id: Optional[int] = Field(None, gt=0)
    start_time: datetime
    end_time: datetime
    capacity: Optional[int] = Field(None, ge=1)

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v


class SessionCreateForEvent(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    speaker_id: Optional[int] = Field(None, gt=0)
    start_time: datetime
    end_time: datetime
    capacity: Optional[int] = Field(None, ge=1)

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v


class SessionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    speaker_id: Optional[int] = Field(None, gt=0)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        if (
            "start_time" in info.data
            and v
            and info.data["start_time"]
            and v <= info.data["start_time"]
        ):
            raise ValueError("end_time must be after start_time")
        return v
