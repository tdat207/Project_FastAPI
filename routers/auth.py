from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.user import (
    UserCreate,
    UserLogin,
    LoginResponse,
    RegisterResponse,
)
from services.auth_service import register_user, login_user
from core.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=RegisterResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = register_user(db, user_data)

    return RegisterResponse(
        message="Đăng ký thành công",
        user=user
    )


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = login_user(
        db,
        login_data.email,
        login_data.password
    )

    access_token = create_access_token(
        {"sub": user.email}
    )

    return LoginResponse(
        message="Đăng nhập thành công",
        access_token=access_token
    )