from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from dependencies.auth import get_current_user
from schemas.event import EventCreate, EventUpdate, EventResponse, EventMemberResponse, AddMemberRequest
from services import event_service

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventResponse)
def create_event_route(event_data: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_service.create_event(db, current_user, event_data)


@router.get("", response_model=list[EventResponse])
def get_events_route(search: Optional[str] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_service.get_events_for_user(db, current_user, search)


@router.get("/{event_id}", response_model=EventResponse)
def get_event_route(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_service.get_event_detail(db, current_user, event_id)


@router.patch("/{event_id}", response_model=EventResponse)
def update_event_route(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_service.update_event(db, current_user, event_id, event_data)


@router.delete("/{event_id}")
def delete_event_route(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event_service.delete_event(db, current_user, event_id)
    return {"detail": "Đã xóa sự kiện"}


@router.post("/{event_id}/members", response_model=EventMemberResponse)
def add_member_route(event_id: int, body: AddMemberRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    staff = event_service.add_member(db, current_user, event_id, body.user_id)
    user = db.query(User).filter(User.id == body.user_id).first()
    return {"user_id": user.id, "email": user.email, "full_name": user.full_name, "role": staff.role}


@router.delete("/{event_id}/members/{user_id}")
def remove_member_route(event_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event_service.remove_member(db, current_user, event_id, user_id)
    return {"detail": "Đã xóa thành viên"}


@router.get("/{event_id}/members", response_model=list[EventMemberResponse])
def list_members_route(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_service.list_members(db, current_user, event_id)