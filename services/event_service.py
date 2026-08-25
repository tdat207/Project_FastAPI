from typing import Optional
from sqlalchemy.orm import Session

from models.event import Event
from models.event_staff import EventStaff
from models.user import User
from schemas.event import EventCreate, EventUpdate
from core.exceptions import NotFoundException, ForbiddenException, BadRequestException


def get_event_or_404(db: Session, event_id: int) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException("Sự kiện không tồn tại")
    return event


def get_staff_record(db: Session, event_id: int, user_id: int):
    return (
        db.query(EventStaff)
        .filter(EventStaff.event_id == event_id, EventStaff.user_id == user_id)
        .first()
    )


def require_member(db: Session, event_id: int, user_id: int) -> EventStaff:
    staff = get_staff_record(db, event_id, user_id)
    if not staff:
        raise ForbiddenException("Bạn không phải thành viên của sự kiện này")
    return staff


def require_owner(db: Session, event_id: int, user_id: int) -> EventStaff:
    staff = require_member(db, event_id, user_id)
    if staff.role != "OWNER":
        raise ForbiddenException("Chỉ OWNER mới được thực hiện thao tác này")
    return staff


def create_event(db: Session, user: User, event_data: EventCreate) -> Event:
    new_event = Event(
        name=event_data.name, description=event_data.description, owner_id=user.id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    staff = EventStaff(event_id=new_event.id, user_id=user.id, role="OWNER")
    db.add(staff)
    db.commit()
    return new_event


def get_events_for_user(db: Session, user: User, search: Optional[str] = None):
    query = (
        db.query(Event)
        .join(EventStaff, EventStaff.event_id == Event.id)
        .filter(EventStaff.user_id == user.id)
    )
    if search:
        query = query.filter(Event.name.ilike(f"%{search}%"))
    return query.all()


def get_event_detail(db: Session, user: User, event_id: int) -> Event:
    event = get_event_or_404(db, event_id)
    require_member(db, event_id, user.id)
    return event


def update_event(
    db: Session, user: User, event_id: int, event_data: EventUpdate
) -> Event:
    event = get_event_or_404(db, event_id)
    require_owner(db, event_id, user.id)

    if event_data.name is not None:
        event.name = event_data.name
    if event_data.description is not None:
        event.description = event_data.description

    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, user: User, event_id: int) -> None:
    event = get_event_or_404(db, event_id)
    require_owner(db, event_id, user.id)
    db.delete(event)
    db.commit()


def add_member(db: Session, user: User, event_id: int, new_user_id: int) -> EventStaff:
    get_event_or_404(db, event_id)
    require_owner(db, event_id, user.id)

    target_user = db.query(User).filter(User.id == new_user_id).first()
    if not target_user:
        raise NotFoundException("Người dùng không tồn tại")

    if get_staff_record(db, event_id, new_user_id):
        raise BadRequestException("Người dùng đã là thành viên của sự kiện")

    staff = EventStaff(event_id=event_id, user_id=new_user_id, role="MEMBER")
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def remove_member(db: Session, user: User, event_id: int, target_user_id: int) -> None:
    get_event_or_404(db, event_id)
    require_owner(db, event_id, user.id)

    staff = get_staff_record(db, event_id, target_user_id)
    if not staff:
        raise NotFoundException("Thành viên không tồn tại trong sự kiện")

    if staff.role == "OWNER":
        owner_count = (
            db.query(EventStaff)
            .filter(EventStaff.event_id == event_id, EventStaff.role == "OWNER")
            .count()
        )
        if owner_count <= 1:
            raise BadRequestException("Không thể xóa OWNER duy nhất của sự kiện")

    db.delete(staff)
    db.commit()


def list_members(db: Session, user: User, event_id: int):
    get_event_or_404(db, event_id)
    require_member(db, event_id, user.id)

    rows = (
        db.query(User.id, User.email, User.full_name, EventStaff.role)
        .join(EventStaff, EventStaff.user_id == User.id)
        .filter(EventStaff.event_id == event_id)
        .all()
    )
    return [
        {"user_id": r.id, "email": r.email, "full_name": r.full_name, "role": r.role}
        for r in rows
    ]
