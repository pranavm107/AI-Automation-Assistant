from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.auth import UserCreateRequest, LoginRequest, RefreshRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.core.permissions import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(request: UserCreateRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register_user(request)

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    # Swagger's form_data provides 'username', which we map to our 'email' field
    request = LoginRequest(email=form_data.username, password=form_data.password)
    return auth_service.login_user(request)

@router.post("/refresh", response_model=dict)
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(request.refresh_token)

@router.post("/logout")
def logout(request: RefreshRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    auth_service.logout_user(request.refresh_token)
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
