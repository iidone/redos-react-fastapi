from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Boolean, Column, Integer, String, Enum, Float, JSON
from sqlalchemy.sql import func
from src.database.database import Base


class KojiCertificate(Base):
    __tablename__ = "koji_certificates"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    issued_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    cert_data: Mapped[str] = mapped_column()
    fingerprint: Mapped[str] = mapped_column()
    private_key: Mapped[str] = mapped_column()
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    revoked = Column(Boolean, default=False)
    permissions = Column(JSON)
    
    organization = relationship("OrganizationsModel")
    issuer = relationship("UsersModel", foreign_keys=[issued_by])