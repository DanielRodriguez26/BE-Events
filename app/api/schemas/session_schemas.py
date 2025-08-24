from datetime import datetime, timedelta
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

    @field_validator("start_time")
    @classmethod
    def start_time_must_be_future(cls, v):
        """Validar que la hora de inicio sea en el futuro"""
        if v <= datetime.now():
            raise ValueError("start_time must be in the future")
        return v

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        """Validar que la hora de fin sea después de la hora de inicio"""
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

    @field_validator("end_time")
    @classmethod
    def session_duration_must_be_reasonable(cls, v, info):
        """Validar que la duración de la sesión sea razonable (entre 15 minutos y 8 horas)"""
        if "start_time" in info.data:
            duration = v - info.data["start_time"]
            min_duration = timedelta(minutes=15)
            max_duration = timedelta(hours=8)
            
            if duration < min_duration:
                raise ValueError("Session duration must be at least 15 minutes")
            if duration > max_duration:
                raise ValueError("Session duration cannot exceed 8 hours")
        return v

    @field_validator("start_time", "end_time")
    @classmethod
    def times_must_be_on_hour_or_half_hour(cls, v):
        """Validar que las horas estén en intervalos de 30 minutos"""
        minute = v.minute
        if minute not in [0, 30]:
            raise ValueError("Times must be on the hour (00) or half hour (30)")
        return v


class SessionCreateForEvent(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    speaker_id: Optional[int] = Field(None, gt=0)
    start_time: datetime
    end_time: datetime
    capacity: Optional[int] = Field(None, ge=1)

    @field_validator("start_time")
    @classmethod
    def start_time_must_be_future(cls, v):
        """Validar que la hora de inicio sea en el futuro"""
        if v <= datetime.now():
            raise ValueError("start_time must be in the future")
        return v

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        """Validar que la hora de fin sea después de la hora de inicio"""
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v

    @field_validator("end_time")
    @classmethod
    def session_duration_must_be_reasonable(cls, v, info):
        """Validar que la duración de la sesión sea razonable (entre 15 minutos y 8 horas)"""
        if "start_time" in info.data:
            duration = v - info.data["start_time"]
            min_duration = timedelta(minutes=15)
            max_duration = timedelta(hours=8)
            
            if duration < min_duration:
                raise ValueError("Session duration must be at least 15 minutes")
            if duration > max_duration:
                raise ValueError("Session duration cannot exceed 8 hours")
        return v

    @field_validator("start_time", "end_time")
    @classmethod
    def times_must_be_on_hour_or_half_hour(cls, v):
        """Validar que las horas estén en intervalos de 30 minutos"""
        minute = v.minute
        if minute not in [0, 30]:
            raise ValueError("Times must be on the hour (00) or half hour (30)")
        return v


class SessionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    speaker_id: Optional[int] = Field(None, gt=0)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None

    @field_validator("start_time")
    @classmethod
    def start_time_must_be_future(cls, v):
        """Validar que la hora de inicio sea en el futuro"""
        if v and v <= datetime.now():
            raise ValueError("start_time must be in the future")
        return v

    @field_validator("end_time")
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        """Validar que la hora de fin sea después de la hora de inicio"""
        if (
            "start_time" in info.data
            and v
            and info.data["start_time"]
            and v <= info.data["start_time"]
        ):
            raise ValueError("end_time must be after start_time")
        return v

    @field_validator("end_time")
    @classmethod
    def session_duration_must_be_reasonable(cls, v, info):
        """Validar que la duración de la sesión sea razonable (entre 15 minutos y 8 horas)"""
        if "start_time" in info.data and v and info.data["start_time"]:
            duration = v - info.data["start_time"]
            min_duration = timedelta(minutes=15)
            max_duration = timedelta(hours=8)
            
            if duration < min_duration:
                raise ValueError("Session duration must be at least 15 minutes")
            if duration > max_duration:
                raise ValueError("Session duration cannot exceed 8 hours")
        return v

    @field_validator("start_time", "end_time")
    @classmethod
    def times_must_be_on_hour_or_half_hour(cls, v):
        """Validar que las horas estén en intervalos de 30 minutos"""
        if v:
            minute = v.minute
            if minute not in [0, 30]:
                raise ValueError("Times must be on the hour (00) or half hour (30)")
        return v
