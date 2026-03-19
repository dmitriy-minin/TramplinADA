import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Table, Column, Integer, Boolean, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


# Many-to-many pivot
opportunity_tags = Table(
    "opportunity_tags",
    Base.metadata,
    Column("opportunity_id", UUID(as_uuid=True), ForeignKey("opportunities.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="tech")  # tech, level, format

    opportunities: Mapped[list["Opportunity"]] = relationship(
        "Opportunity", secondary=opportunity_tags, back_populates="tags"
    )


class OpportunityType(str, enum.Enum):
    VACANCY = "vacancy"
    INTERNSHIP = "internship"
    MENTORSHIP = "mentorship"
    EVENT = "event"


class WorkFormat(str, enum.Enum):
    OFFICE = "office"
    REMOTE = "remote"
    HYBRID = "hybrid"


class ExperienceLevel(str, enum.Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    ANY = "any"


class OpportunityStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REJECTED = "rejected"
    CLOSED = "closed"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id"))
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[OpportunityType] = mapped_column(Enum(OpportunityType), nullable=False)
    format: Mapped[WorkFormat] = mapped_column(Enum(WorkFormat), nullable=False)
    level: Mapped[ExperienceLevel] = mapped_column(Enum(ExperienceLevel), default=ExperienceLevel.ANY)
    status: Mapped[OpportunityStatus] = mapped_column(Enum(OpportunityStatus), default=OpportunityStatus.PENDING)
    
    salary_from: Mapped[int | None] = mapped_column(Integer)
    salary_to: Mapped[int | None] = mapped_column(Integer)
    salary_currency: Mapped[str] = mapped_column(String(10), default="KZT")
    
    address: Mapped[str | None] = mapped_column(String(500))
    city: Mapped[str | None] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    
    media_urls: Mapped[str | None] = mapped_column(Text)  # JSON array stored as text
    rejection_reason: Mapped[str | None] = mapped_column(Text)
    
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="opportunities")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=opportunity_tags, back_populates="opportunities")
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="opportunity")
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="opportunity")
