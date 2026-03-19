from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Неверный тип токена")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Пользователь не найден или деактивирован")
    
    return user


async def get_current_active_employer(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.EMPLOYER:
        raise HTTPException(status_code=403, detail="Доступ только для работодателей")
    return user


async def get_current_curator(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.CURATOR:
        raise HTTPException(status_code=403, detail="Доступ только для кураторов")
    return user


async def get_current_main_admin(user: User = Depends(get_current_curator)) -> User:
    if not user.is_main_admin:
        raise HTTPException(status_code=403, detail="Доступ только для главного администратора")
    return user


def optional_auth(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    return credentials
