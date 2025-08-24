from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventRegistrationCreate(BaseModel):
    """Esquema para crear un registro de evento"""

    event_id: int = Field(..., description="ID del evento al que se registra")
    number_of_participants: int = Field(
        ..., ge=1, le=10, description="Número de participantes (máximo 10)"
    )

    @field_validator("number_of_participants")
    @classmethod
    def validate_participants(cls, v):
        """Valida que el número de participantes esté en el rango permitido"""
        if v < 1:
            raise ValueError("El número de participantes debe ser al menos 1")
        if v > 10:
            raise ValueError("El número máximo de participantes por registro es 10")
        return v


class EventRegistrationUpdate(BaseModel):
    """Esquema para actualizar un registro de evento"""

    number_of_participants: int = Field(
        ..., ge=1, le=10, description="Número de participantes (máximo 10)"
    )

    @field_validator("number_of_participants")
    @classmethod
    def validate_participants(cls, v):
        """Valida que el número de participantes esté en el rango permitido"""
        if v < 1:
            raise ValueError("El número de participantes debe ser al menos 1")
        if v > 10:
            raise ValueError("El número máximo de participantes por registro es 10")
        return v


class EventRegistration(BaseModel):
    """Esquema para representar un registro de evento"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    user_id: int
    number_of_participants: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class EventRegistrationWithEvent(BaseModel):
    """Esquema para representar un registro de evento con información del evento"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    user_id: int
    number_of_participants: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    title: str
    date: datetime
    location: str
    start_date: datetime
    end_date: datetime
