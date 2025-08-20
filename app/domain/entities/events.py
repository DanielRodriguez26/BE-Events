import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(
        ..., min_length=1, max_length=255, description="Título del evento"
    )
    description: Optional[str] = Field(None, description="Descripción del evento")
    date: datetime = Field(..., description="Fecha y hora del evento")
    location: Optional[str] = Field(
        None, max_length=255, description="Ubicación del evento"
    )
    is_active: bool = Field(True, description="Estado activo del evento")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización")

    class Config:
        from_attributes = True  # Para Pydantic v2
        populate_by_name = True  # Para Pydantic v2
        json_encoders = {datetime: lambda v: v.isoformat()}
