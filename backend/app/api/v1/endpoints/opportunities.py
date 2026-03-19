from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
import uuid

from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.opportunity import Opportunity, Tag, OpportunityStatus, OpportunityType, WorkFormat, ExperienceLevel
from app.models.company import Company
from app.models.application import Favorite, Application
from app.schemas.opportunity import (
    OpportunityCreate, OpportunityUpdate, OpportunityResponse,
    OpportunityListResponse, OpportunityModerate
)
from app.core.deps import get_current_user, get_current_active_employer, get_current_curator, optional_auth

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


def opportunity_options():
    return selectinload(Opportunity.tags), selectinload(Opportunity.company), selectinload(Opportunity.applications)


@router.get("", response_model=OpportunityListResponse)
async def list_opportunities(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    type: Optional[OpportunityType] = None,
    format: Optional[WorkFormat] = None,
    level: Optional[ExperienceLevel] = None,
    salary_from: Optional[int] = None,
    salary_to: Optional[int] = None,
    tag_ids: Optional[str] = None,
    city: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    credentials=Depends(optional_auth),
):
    filters = [Opportunity.status == OpportunityStatus.ACTIVE]

    if search:
        filters.append(
            or_(
                Opportunity.title.ilike(f"%{search}%"),
                Opportunity.description.ilike(f"%{search}%"),
            )
        )
    if type:
        filters.append(Opportunity.type == type)
    if format:
        filters.append(Opportunity.format == format)
    if level:
        filters.append(Opportunity.level == level)
    if salary_from is not None:
        filters.append(Opportunity.salary_from >= salary_from)
    if salary_to is not None:
        filters.append(Opportunity.salary_to <= salary_to)
    if city:
        filters.append(Opportunity.city.ilike(f"%{city}%"))

    query = (
        select(Opportunity)
        .options(*opportunity_options())
        .where(and_(*filters))
        .order_by(Opportunity.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    if tag_ids:
        ids = [uuid.UUID(t) for t in tag_ids.split(",")]
        query = query.where(Opportunity.tags.any(Tag.id.in_(ids)))

    count_query = select(func.count(Opportunity.id)).where(and_(*filters))
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    return OpportunityListResponse(
        items=[OpportunityResponse(
            **{k: v for k, v in vars(o).items() if not k.startswith("_")},
            applications_count=len(o.applications),
        ) for o in items],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Opportunity)
        .options(*opportunity_options())
        .where(Opportunity.id == opportunity_id)
    )
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Возможность не найдена")

    # Increment views
    opp.views_count += 1
    await db.commit()
    await db.refresh(opp)

    return OpportunityResponse(
        **{k: v for k, v in vars(opp).items() if not k.startswith("_")},
        applications_count=len(opp.applications),
    )


@router.post("", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(
    data: OpportunityCreate,
    current_user: User = Depends(get_current_active_employer),
    db: AsyncSession = Depends(get_db),
):
    company_result = await db.execute(
        select(Company).where(Company.owner_id == current_user.id)
    )
    company = company_result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Профиль компании не найден")

    tags = []
    if data.tag_ids:
        tags_result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        tags = tags_result.scalars().all()

    opp = Opportunity(
        company_id=company.id,
        title=data.title,
        description=data.description,
        type=data.type,
        format=data.format,
        level=data.level,
        salary_from=data.salary_from,
        salary_to=data.salary_to,
        salary_currency=data.salary_currency,
        address=data.address,
        city=data.city,
        latitude=data.latitude,
        longitude=data.longitude,
        expires_at=data.expires_at,
        tags=tags,
    )
    db.add(opp)
    await db.commit()
    await db.refresh(opp)
    
    result = await db.execute(
        select(Opportunity).options(*opportunity_options()).where(Opportunity.id == opp.id)
    )
    opp = result.scalar_one()
    return OpportunityResponse(**{k: v for k, v in vars(opp).items() if not k.startswith("_")}, applications_count=0)


@router.patch("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: uuid.UUID,
    data: OpportunityUpdate,
    current_user: User = Depends(get_current_active_employer),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Opportunity)
        .options(*opportunity_options())
        .where(Opportunity.id == opportunity_id)
    )
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Возможность не найдена")
    if str(opp.company.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Нет доступа")

    update_data = data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for field, value in update_data.items():
        setattr(opp, field, value)

    if data.tag_ids is not None:
        tags_result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        opp.tags = tags_result.scalars().all()

    opp.status = OpportunityStatus.PENDING  # Re-moderate on edit
    await db.commit()
    await db.refresh(opp)
    return OpportunityResponse(**{k: v for k, v in vars(opp).items() if not k.startswith("_")}, applications_count=len(opp.applications))


@router.delete("/{opportunity_id}", status_code=204)
async def delete_opportunity(
    opportunity_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Opportunity).options(selectinload(Opportunity.company)).where(Opportunity.id == opportunity_id)
    )
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Не найдено")
    
    if current_user.role != UserRole.CURATOR:
        if str(opp.company.owner_id) != str(current_user.id):
            raise HTTPException(status_code=403, detail="Нет доступа")

    await db.delete(opp)
    await db.commit()


@router.post("/{opportunity_id}/moderate", response_model=OpportunityResponse)
async def moderate_opportunity(
    opportunity_id: uuid.UUID,
    data: OpportunityModerate,
    current_user: User = Depends(get_current_curator),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Opportunity).options(*opportunity_options()).where(Opportunity.id == opportunity_id)
    )
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Не найдено")

    opp.status = data.status
    opp.rejection_reason = data.rejection_reason
    await db.commit()
    await db.refresh(opp)
    return OpportunityResponse(**{k: v for k, v in vars(opp).items() if not k.startswith("_")}, applications_count=len(opp.applications))
