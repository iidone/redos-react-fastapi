from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CertificateBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    organization_id: int = Field(..., description="ID организации")
    issued_by: int = Field(..., description="ID пользователя, выдавшего сертификат")
    permissions: List[str] = Field(..., example=["build", "repo"], description="Список разрешений")
    expires_at: datetime = Field(..., description="Срок действия сертификата")

class CertificateCreate(CertificateBase):
    pass

class CertificateUpdate(BaseModel):
    is_revoked: Optional[bool] = Field(None, description="Отозван ли сертификат")

class CertificateResponce(CertificateBase):
    id: int
    is_revoked: bool
    created_at: datetime

    class Config:
        from_attributes = True