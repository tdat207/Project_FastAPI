from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EventTaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: str = "MEDIUM"


class EventTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    priority: str | None = None
    status: str | None = None
    assigned_to: int | None = None


class EventTaskResponse(BaseModel):
    id: int
    event_id: int
    title: str
    description: str | None = None
    status: str
    priority: str
    due_date: datetime | None = None
    assigned_to: int | None = None

    model_config = ConfigDict(from_attributes=True)