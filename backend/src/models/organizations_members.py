from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base

class OrganizationsMembersModel(Base):
    __tablename__ = "organization_members"
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        primary_key=True
    )
    assigned_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )