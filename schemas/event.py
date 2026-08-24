from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: str
    description: str | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class EventResponse(EventBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class EventMemberResponse(BaseModel):
    user_id: int
    email: str
    full_name: str | None = None
    role: str


class AddMemberRequest(BaseModel):
    user_id: int