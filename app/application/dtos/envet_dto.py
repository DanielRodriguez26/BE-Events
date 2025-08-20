import uuid
from pydantic import BaseModel

class EventDTO(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    date: str
    location: str

    class Config:
        orm_mode = True
