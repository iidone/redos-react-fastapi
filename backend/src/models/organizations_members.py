from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base

class OrganizationsMembersModel(Base):
    __tablename__ = "organization_members"

    member_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="fk_member"),
        primary_key=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        primary_key=True
    )

    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="fk_organizer"),
        nullable=False
    )
    
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
