from fastapi import FastAPI
from db.database import Base, engine
from models import user, event, event_staff, event_task
from core.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException,
    not_found_handler,
    bad_request_handler,
    forbidden_handler,
)
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.events import router as events_router
from routers.event_tasks import router as event_tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(BadRequestException, bad_request_handler)
app.add_exception_handler(ForbiddenException, forbidden_handler)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(events_router)
app.include_router(event_tasks_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}