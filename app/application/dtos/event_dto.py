import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventDTO(BaseModel):
    id: Optional[uuid.UUID] = None
    title: str = Field(
        ..., min_length=1, max_length=255, description="Título del evento"
    )
    description: Optional[str] = Field(None, description="Descripción del evento")
    date: datetime = Field(..., description="Fecha y hora del evento")
    location: Optional[str] = Field(
        None, max_length=255, description="Ubicación del evento"
    )
    is_active: bool = Field(True, description="Estado activo del evento")

    class Config:
        from_attributes = True  # Para SQLAlchemy 2.0+
        json_encoders = {datetime: lambda v: v.isoformat()}


class CreateEventDTO(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=255, description="Título del evento"
    )
    description: Optional[str] = Field(None, description="Descripción del evento")
    date: datetime = Field(..., description="Fecha y hora del evento")
    location: Optional[str] = Field(
        None, max_length=255, description="Ubicación del evento"
    )
    is_active: bool = Field(True, description="Estado activo del evento")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class UpdateEventDTO(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Título del evento"
    )
    description: Optional[str] = Field(None, description="Descripción del evento")
    date: Optional[datetime] = Field(None, description="Fecha y hora del evento")
    location: Optional[str] = Field(
        None, max_length=255, description="Ubicación del evento"
    )
    is_active: Optional[bool] = Field(None, description="Estado activo del evento")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
