from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from db.database import Base


class EventTask(Base):
    __tablename__ = "event_tasks"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(String(20), default="TODO")
    priority = Column(String(20), default="MEDIUM")
    due_date = Column(DateTime, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())