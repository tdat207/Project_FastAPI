from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import User
from dependencies.auth import get_current_user
from schemas.event_task import EventTaskCreate, EventTaskUpdate, EventTaskResponse
from services import event_task_service

router = APIRouter(tags=["Event Tasks"])


@router.post("/events/{event_id}/event-tasks", response_model=EventTaskResponse)
def create_task_route(event_id: int, data: EventTaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_task_service.create_task(db, current_user, event_id, data)


@router.get("/events/{event_id}/event-tasks", response_model=list[EventTaskResponse])
def get_tasks_route(
    event_id: int,
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assignee: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return event_task_service.get_tasks(
        db, current_user, event_id, status, priority, assignee, search, limit, offset, sort_by, order
    )


@router.get("/event-tasks/{task_id}", response_model=EventTaskResponse)
def get_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_task_service.get_task_detail(db, current_user, task_id)


@router.patch("/event-tasks/{task_id}", response_model=EventTaskResponse)
def update_task_route(task_id: int, data: EventTaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return event_task_service.update_task(db, current_user, task_id, data)


@router.delete("/event-tasks/{task_id}")
def delete_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event_task_service.delete_task(db, current_user, task_id)
    return {"detail": "Đã xóa công việc"}