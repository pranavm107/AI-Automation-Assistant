from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.services.password_service import PasswordService
from app.services.jwt_service import JWTService
from app.schemas.auth import UserCreateRequest, LoginRequest
from app.models.user import User
from app.models.refresh_token import RefreshToken
from datetime import datetime, timezone

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, data: UserCreateRequest) -> User:
        if self.user_repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if self.user_repo.get_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        hashed_pw = PasswordService.hash_password(data.password)
        new_user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            hashed_password=hashed_pw
        )
        return self.user_repo.create(new_user)

    def login_user(self, data: LoginRequest):
        user = self.user_repo.get_by_email(data.email)
        if not user or not PasswordService.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

        user.last_login = datetime.now(timezone.utc)
        self.user_repo.update(user)

        access_token = JWTService.create_access_token(subject=str(user.id))
        refresh_token_str = JWTService.create_refresh_token(subject=str(user.id))

        # Store refresh token
        db_token = RefreshToken(
            user_id=user.id,
            token_hash=PasswordService.hash_password(refresh_token_str),
            expires_at=datetime.now(timezone.utc) # Will be properly set in the model, but let's just abstract for now
        )
        self.db.add(db_token)
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "bearer",
            "expires_in": 3600
        }

    def refresh_access_token(self, refresh_token: str):
        payload = JWTService.decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload")

        # Verify token exists and is not revoked
        # For full implementation we should check token_hash against the DB.
        
        new_access_token = JWTService.create_access_token(subject=user_id)
        return {"access_token": new_access_token}

    def logout_user(self, refresh_token: str):
        # Ideally we find the refresh token and mark it as revoked
        pass
