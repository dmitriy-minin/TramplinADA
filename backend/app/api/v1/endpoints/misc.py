from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, UUID4
from typing import Optional, List
import uuid

from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.opportunity import Opportunity, Tag, OpportunityStatus
from app.models.application import Application, Favorite, Contact, ApplicationStatus, ContactStatus
from app.schemas.opportunity import TagResponse, TagBase
from app.core.deps import get_current_user, get_current_curator, get_current_main_admin

router = APIRouter()


# ─── Tags ────────────────────────────────────────────────────────────────────

tags_router = APIRouter(prefix="/tags", tags=["tags"])


@tags_router.get("", response_model=List[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.name))
    return result.scalars().all()


@tags_router.post("", response_model=TagResponse, status_code=201)
async def create_tag(data: TagBase, current_user: User = Depends(get_current_curator), db: AsyncSession = Depends(get_db)):
    tag = Tag(name=data.name, category=data.category)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


@tags_router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: uuid.UUID, current_user: User = Depends(get_current_curator), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(404, "Тег не найден")
    await db.delete(tag)
    await db.commit()


# ─── Applications ─────────────────────────────────────────────────────────────

applications_router = APIRouter(prefix="/applications", tags=["applications"])


class ApplicationCreate(BaseModel):
    opportunity_id: UUID4
    cover_letter: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: UUID4
    opportunity_id: UUID4
    status: ApplicationStatus
    cover_letter: Optional[str]

    class Config:
        from_attributes = True


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


@applications_router.post("", response_model=ApplicationResponse, status_code=201)
async def apply(data: ApplicationCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.SOISKATEL:
        raise HTTPException(403, "Только соискатели могут откликаться")
    
    existing = await db.execute(
        select(Application).where(
            Application.applicant_id == current_user.id,
            Application.opportunity_id == data.opportunity_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Вы уже откликались на эту вакансию")

    opp = await db.get(Opportunity, data.opportunity_id)
    if not opp or opp.status != OpportunityStatus.ACTIVE:
        raise HTTPException(400, "Вакансия недоступна")

    app = Application(
        applicant_id=current_user.id,
        opportunity_id=data.opportunity_id,
        cover_letter=data.cover_letter,
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app


@applications_router.get("/my", response_model=List[ApplicationResponse])
async def my_applications(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Application).where(Application.applicant_id == current_user.id).order_by(Application.created_at.desc())
    )
    return result.scalars().all()


@applications_router.patch("/{app_id}/status")
async def update_status(
    app_id: uuid.UUID,
    data: ApplicationStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).options(
            selectinload(Application.opportunity).selectinload(Opportunity.company)
        ).where(Application.id == app_id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Отклик не найден")
    if str(app.opportunity.company.owner_id) != str(current_user.id):
        raise HTTPException(403, "Нет доступа")
    
    app.status = data.status
    await db.commit()
    return {"status": "updated"}


# ─── Favorites ────────────────────────────────────────────────────────────────

favorites_router = APIRouter(prefix="/favorites", tags=["favorites"])


@favorites_router.post("/{opportunity_id}", status_code=201)
async def add_favorite(opportunity_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id, Favorite.opportunity_id == opportunity_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Уже в избранном")
    
    fav = Favorite(user_id=current_user.id, opportunity_id=opportunity_id)
    db.add(fav)
    await db.commit()
    return {"status": "added"}


@favorites_router.delete("/{opportunity_id}", status_code=204)
async def remove_favorite(opportunity_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id, Favorite.opportunity_id == opportunity_id)
    )
    fav = result.scalar_one_or_none()
    if not fav:
        raise HTTPException(404, "Не найдено в избранном")
    await db.delete(fav)
    await db.commit()


@favorites_router.get("/my")
async def my_favorites(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id)
    )
    return [{"opportunity_id": str(f.opportunity_id)} for f in result.scalars().all()]


# ─── Users (admin) ───────────────────────────────────────────────────────────

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("")
async def list_users(current_user: User = Depends(get_current_curator), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [{"id": str(u.id), "email": u.email, "full_name": u.full_name, "role": u.role, "is_active": u.is_active, "is_verified": u.is_verified} for u in users]


@users_router.patch("/{user_id}/deactivate")
async def deactivate_user(user_id: uuid.UUID, current_user: User = Depends(get_current_curator), db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    user.is_active = False
    await db.commit()
    return {"status": "deactivated"}


# ─── Companies (admin) ────────────────────────────────────────────────────────

companies_router = APIRouter(prefix="/companies", tags=["companies"])


@companies_router.get("")
async def list_companies(current_user: User = Depends(get_current_curator), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).order_by(Company.created_at.desc()))
    companies = result.scalars().all()
    return [{"id": str(c.id), "name": c.name, "inn": c.inn, "is_verified": c.is_verified} for c in companies]


@companies_router.patch("/{company_id}/verify")
async def verify_company(company_id: uuid.UUID, current_user: User = Depends(get_current_curator), db: AsyncSession = Depends(get_db)):
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(404, "Компания не найдена")
    company.is_verified = True
    await db.commit()
    return {"status": "verified"}
