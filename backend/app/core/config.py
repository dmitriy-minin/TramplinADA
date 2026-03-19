from pydantic_settings import BaseSettings
from typing import List
import secrets


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Трамплин"
    DEBUG: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/tramplin"
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Email (Resend)
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@tramplin.kz"
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    # Admin seed
    ADMIN_EMAIL: str = "admin@tramplin.kz"
    ADMIN_PASSWORD: str = "Admin123!@#"
    ADMIN_NAME: str = "Главный администратор"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
