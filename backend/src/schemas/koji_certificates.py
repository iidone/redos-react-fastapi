from pydantic import BaseModel, Field, model_serializer
from datetime import datetime
from typing import List, Optional, Dict

class KojiCertificateBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    organization_id: int = Field(..., description="ID организации")
    issued_by: int = Field(..., description="ID пользователя, выдавшего сертификат")
    valid_from: datetime = Field(..., description="Дата начала действия")
    valid_to: datetime = Field(..., description="Дата окончания действия")
    revoked: bool = Field(default=False, description="Отозван ли сертификат")
    permissions: Dict[str, bool] = Field(
        default={},
        description="Права доступа в формате {'build': True, 'admin': False}"
    )

    class Config:
        from_attributes = True
    
    
class CertificateUpdate(BaseModel):
    revoked: Optional[bool] = Field(None, description="Отозвать сертификат")
    permissions: Optional[Dict[str, bool]] = Field(
        None,
        description="Обновленные права доступа"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "revoked": True,
                "permissions": {"build": False, "admin": False, "repo": False}
            }
        }

class CertificateRequest(BaseModel):
    user_id: int
    organization_id: int
    valid_days: int = 30
    permissions: Dict[str, bool] = {
        "build": False,
        "repo": False,
        "admin": False,
    }

class CertificateResponse(BaseModel):
    id: int = Field(..., description="ID сертификата")
    organization_id: int = Field(..., description="ID организации")
    organization_name: str = Field(..., description="Название организации")
    issued_by: int = Field(..., description="ID пользователя, выдавшего сертификат")
    issued_by_name: str = Field(..., description="Имя пользователя, выдавшего сертификат")
    valid_from: datetime = Field(..., description="Дата начала действия")
    valid_to: datetime = Field(..., description="Дата окончания действия")
    permissions: Dict[str, bool] = Field(
        default={},
        description="Права доступа в формате {'build': True, 'admin': False}"
    )
    revoked: bool = Field(..., description="Отозван ли сертификат")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "organization_id": 1,
                "issued_by": 1,
                "cert_data": None,
                "private_key": None,
                "valid_from": "2023-01-01T00:00:00",
                "valid_to": "2024-01-01T00:00:00",
                "revoked": False,
                "permissions": {"build": True, "admin": False, "repo": True}
            }
        }
        
        
class KojiCertificateAdminResponse(CertificateResponse):
    cert_data: str = Field(..., description="Данные сертификата в PEM формате")
    fingerprint: str = Field(..., description="SHA-256 отпечаток сертификата")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "organization_id": 1,
                "issued_by": 1,
                "cert_data": "-----BEGIN CERTIFICATE-----...",
                "fingerprint": "3a2b1c...",
                "valid_from": "2023-01-01T00:00:00",
                "valid_to": "2024-01-01T00:00:00",
                "revoked": False,
                "permissions": {"build": True, "admin": False}
            }
        }
    

    