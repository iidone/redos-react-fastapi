from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base

class OrganizationsMembersModel(Base):
    __tablename__ = "organizations_members"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    member_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )
    
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
