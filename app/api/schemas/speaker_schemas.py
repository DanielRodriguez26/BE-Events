# id, name, email, phone, bio, company,

import datetime
from typing import Optional

from pydantic import BaseModel


class Speaker(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    bio: str
    company: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True
