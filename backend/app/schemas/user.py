from pydantic import BaseModel, EmailStr, field_validator, UUID4
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, PrivacyLevel
from app.core.security import validate_password_strength


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole
    # Employer fields
    company_name: Optional[str] = None
    inn: Optional[str] = None
    # Soiskatel fields
    university: Optional[str] = None
    study_year: Optional[int] = None

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v):
        if not validate_password_strength(v):
            raise ValueError("Пароль должен содержать минимум 8 символов, одну заглавную букву и цифру")
        return v

    @field_validator("role")
    @classmethod
    def role_not_curator(cls, v):
        if v == UserRole.CURATOR:
            raise ValueError("Нельзя зарегистрироваться как куратор")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: UUID4
    email: str
    full_name: str
    role: UserRole
    is_verified: bool
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    university: Optional[str] = None
    study_year: Optional[int] = None
    resume_markdown: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume_privacy: Optional[PrivacyLevel] = None


class UserPublicProfile(BaseModel):
    id: UUID4
    full_name: str
    role: UserRole
    avatar_url: Optional[str]
    university: Optional[str]
    study_year: Optional[int]
    bio: Optional[str]
    github_url: Optional[str]
    portfolio_url: Optional[str]
    resume_markdown: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
