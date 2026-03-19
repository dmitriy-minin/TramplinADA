from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime
from app.models.opportunity import OpportunityType, WorkFormat, ExperienceLevel, OpportunityStatus


class TagBase(BaseModel):
    name: str
    category: str = "tech"


class TagResponse(TagBase):
    id: UUID4

    class Config:
        from_attributes = True


class CompanyShort(BaseModel):
    id: UUID4
    name: str
    logo_url: Optional[str]
    city: Optional[str]
    is_verified: bool

    class Config:
        from_attributes = True


class OpportunityCreate(BaseModel):
    title: str
    description: str
    type: OpportunityType
    format: WorkFormat
    level: ExperienceLevel = ExperienceLevel.ANY
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    salary_currency: str = "KZT"
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tag_ids: List[UUID4] = []
    expires_at: Optional[datetime] = None


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[OpportunityType] = None
    format: Optional[WorkFormat] = None
    level: Optional[ExperienceLevel] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tag_ids: Optional[List[UUID4]] = None
    expires_at: Optional[datetime] = None


class OpportunityResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    type: OpportunityType
    format: WorkFormat
    level: ExperienceLevel
    status: OpportunityStatus
    salary_from: Optional[int]
    salary_to: Optional[int]
    salary_currency: str
    address: Optional[str]
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    views_count: int
    tags: List[TagResponse]
    company: CompanyShort
    created_at: datetime
    expires_at: Optional[datetime]
    applications_count: Optional[int] = None
    is_favorited: Optional[bool] = None

    class Config:
        from_attributes = True


class OpportunityListResponse(BaseModel):
    items: List[OpportunityResponse]
    total: int
    page: int
    per_page: int
    pages: int


class OpportunityModerate(BaseModel):
    status: OpportunityStatus
    rejection_reason: Optional[str] = None
