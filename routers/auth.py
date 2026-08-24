from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user import UserCreate, UserResponse, UserLogin, Token
from services.auth_service import register_user, login_user
from core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data)

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = login_user(db, login_data.email, login_data.password)
    access_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token)