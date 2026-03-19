import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    RESERVE = "reserve"


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("applicant_id", "opportunity_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    applicant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    opportunity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("opportunities.id"))
    
    cover_letter: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.PENDING
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    applicant: Mapped["User"] = relationship("User", back_populates="applications")
    opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="applications")


class ContactStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint("requester_id", "recipient_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    recipient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    status: Mapped[ContactStatus] = mapped_column(Enum(ContactStatus), default=ContactStatus.PENDING)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    requester: Mapped["User"] = relationship("User", foreign_keys=[requester_id], back_populates="sent_contacts")
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id], back_populates="received_contacts")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "opportunity_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    opportunity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("opportunities.id"))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="favorites")
