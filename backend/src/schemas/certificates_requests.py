from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class CertificateRequestBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя, запросившего сертификат")
    status: RequestStatus = Field(default=RequestStatus.PENDING, description="Статус запроса")

class CertificateRequestCreate(CertificateRequestBase):
    pass

class CertificateRequestUpdate(BaseModel):
    status: RequestStatus = Field(..., description="Новый статус запроса")
    processed_by: int = Field(..., description="ID пользователя, обработавшего запрос")

class CertificateRequest(CertificateRequestBase):
    id: int
    processed_by: Optional[int] = Field(None, description="ID обработавшего администратора")
    created_at: datetime
    
    class Config:
        from_attributes = True  # Для SQLAlchemy