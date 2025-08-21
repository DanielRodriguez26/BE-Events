import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import func
from sqlalchemy import DateTime as SADateTime


class EventModel(SQLModel, table=True):
    __tablename__ = "events"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    date: datetime = Field(nullable=False, sa_type=SADateTime(timezone=True))
    location: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True, nullable=False)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_type=SADateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=SADateTime(timezone=True),
        sa_column_kwargs={"onupdate": func.now()},
    )

