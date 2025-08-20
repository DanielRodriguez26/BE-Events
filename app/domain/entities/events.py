import uuid
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    description: str
    date: str
    location: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True