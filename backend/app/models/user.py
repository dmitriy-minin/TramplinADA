import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class UserRole(str, enum.Enum):
    SOISKATEL = "soiskatel"
    EMPLOYER = "employer"
    CURATOR = "curator"


class PrivacyLevel(str, enum.Enum):
    PUBLIC = "public"
    CONTACTS_ONLY = "contacts_only"
    HIDDEN = "hidden"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    
    # Profile fields (soiskatel)
    university: Mapped[str | None] = mapped_column(String(255))
    study_year: Mapped[int | None] = mapped_column()
    bio: Mapped[str | None] = mapped_column(Text)
    resume_markdown: Mapped[str | None] = mapped_column(Text)
    github_url: Mapped[str | None] = mapped_column(String(500))
    portfolio_url: Mapped[str | None] = mapped_column(String(500))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    resume_privacy: Mapped[PrivacyLevel] = mapped_column(
        Enum(PrivacyLevel), default=PrivacyLevel.PUBLIC
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_main_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="owner", uselist=False)
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="applicant")
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user")
    sent_contacts: Mapped[list["Contact"]] = relationship(
        "Contact", foreign_keys="Contact.requester_id", back_populates="requester"
    )
    received_contacts: Mapped[list["Contact"]] = relationship(
        "Contact", foreign_keys="Contact.recipient_id", back_populates="recipient"
    )
