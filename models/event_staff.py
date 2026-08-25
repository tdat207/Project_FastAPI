from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base


class EventStaff(Base):
    __tablename__ = "evemt_staff"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20), default="MEMBER")
