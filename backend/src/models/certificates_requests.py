from enum import Enum as PyEnum
from sqlalchemy import Enum, ForeignKey, DateTime, String, func, CheckConstraint
from datetime import datetime
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

class RequestStatus(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class CertificatesRequestsModel(Base):
    __tablename__ = "certificates_requests"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default=RequestStatus.PENDING.value,
        server_default=RequestStatus.PENDING.value,
        nullable=False
    )
    processed_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name="ck_certificates_requests_status"
        ),
    )