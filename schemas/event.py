from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    description: str | None = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True