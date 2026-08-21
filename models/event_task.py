from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class EventTask(Base):
    __tablename__ = "event_tasks"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    title = Column(String(255), nullable=False)
    status = Column(String(20), default="TODO")
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable = True)