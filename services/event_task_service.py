from typing import Optional
from sqlalchemy.orm import Session

from models.event_task import EventTask
from models.event_staff import EventStaff
from models.user import User
from schemas.event_task import EventTaskCreate, EventTaskUpdate
from core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from services.event_service import get_event_or_404, require_member, get_staff_record

ALLOWED_STATUS = {"TODO", "IN_PROGRESS", "DONE"}
ALLOWED_PRIORITY = {"LOW", "MEDIUM", "HIGH"}


def get_task_or_404(db: Session, task_id: int) -> EventTask:
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        raise NotFoundException("Công việc không tồn tại")
    return task


def create_task(db: Session, user: User, event_id: int, data: EventTaskCreate) -> EventTask:
    get_event_or_404(db, event_id)
    require_member(db, event_id, user.id)

    if not data.title or not data.title.strip():
        raise BadRequestException("Tên công việc không được để trống")
    if data.priority not in ALLOWED_PRIORITY:
        raise BadRequestException("Priority không hợp lệ (LOW/MEDIUM/HIGH)")

    task = EventTask(
        event_id=event_id,
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        priority=data.priority,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session, user: User, event_id: int,
    status: Optional[str] = None, priority: Optional[str] = None,
    assignee: Optional[int] = None, search: Optional[str] = None,
    limit: int = 10, offset: int = 0,
    sort_by: str = "created_at", order: str = "desc",
):
    get_event_or_404(db, event_id)
    require_member(db, event_id, user.id)

    query = db.query(EventTask).filter(EventTask.event_id == event_id)

    if status:
        query = query.filter(EventTask.status == status)
    if priority:
        query = query.filter(EventTask.priority == priority)
    if assignee:
        query = query.filter(EventTask.assigned_to == assignee)
    if search:
        query = query.filter(EventTask.title.ilike(f"%{search}%"))

    sort_column = EventTask.due_date if sort_by == "due_date" else EventTask.created_at
    query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    return query.offset(offset).limit(limit).all()


def get_task_detail(db: Session, user: User, task_id: int) -> EventTask:
    task = get_task_or_404(db, task_id)
    require_member(db, task.event_id, user.id)
    return task


def update_task(db: Session, user: User, task_id: int, data: EventTaskUpdate) -> EventTask:
    task = get_task_or_404(db, task_id)
    staff = require_member(db, task.event_id, user.id)

    is_owner = staff.role == "OWNER"
    is_assignee = task.assigned_to == user.id
    if not is_owner and not is_assignee:
        raise ForbiddenException("Chỉ OWNER hoặc người được giao mới được sửa công việc này")

    if data.status is not None:
        if data.status not in ALLOWED_STATUS:
            raise BadRequestException("Status không hợp lệ (TODO/IN_PROGRESS/DONE)")
        task.status = data.status
    if data.priority is not None:
        if data.priority not in ALLOWED_PRIORITY:
            raise BadRequestException("Priority không hợp lệ (LOW/MEDIUM/HIGH)")
        task.priority = data.priority
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.due_date is not None:
        task.due_date = data.due_date
    if data.assigned_to is not None:
        if not is_owner:
            raise ForbiddenException("Chỉ OWNER mới được giao việc")
        if not get_staff_record(db, task.event_id, data.assigned_to):
            raise BadRequestException("Người được giao phải là thành viên của sự kiện")
        task.assigned_to = data.assigned_to

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user: User, task_id: int) -> None:
    task = get_task_or_404(db, task_id)
    staff = require_member(db, task.event_id, user.id)
    if staff.role != "OWNER":
        raise ForbiddenException("Chỉ OWNER mới được xóa công việc")
    db.delete(task)
    db.commit()