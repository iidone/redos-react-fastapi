from fastapi import APIRouter, Depends, HTTPException, status
from cryptography.hazmat.primitives import serialization, hashes
from sqlalchemy.ext.asyncio import AsyncSession
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from fastapi import HTTPException
from sqlalchemy.future import select
from src.models.organizations import OrganizationsModel
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from typing_extensions import Annotated
from src.models.organizations_members import OrganizationsMembersModel
import base64
from src.schemas.koji_certificates import CertificateResponse, CertificateRequest
from src.services.auth import SessionDep, get_current_user
from src.models.users import UsersModel
from src.models.koji_certificates import KojiCertificate
from src.services.GenerateCert import generate_koji_cert
import logger
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import os
from src.services.ca_init import init_ca, _CA_CACHE
from typing_extensions import List


router = APIRouter(prefix="/v1/certificates", tags=["Сертификаты"])


@router.post("/", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED, summary= "Создать Koji сертификат")
async def create_koji_certificate(
    request: CertificateRequest,
    session: SessionDep,
    current_user: UsersModel = Depends(get_current_user)
):
    try:
        if not os.path.exists("certs/ca.crt"):
            init_ca()

        if not await check_cert_permissions(current_user, request.user_id, session):
            raise HTTPException(status_code=403, detail="Not enough permissions")

        cert_pem, key_pem = await generate_koji_cert(
            user_id=request.user_id,
            valid_days=request.valid_days,
            ca_cert=get_ca_cert(),
            ca_private_key=get_ca_key(),
            permissions=request.permissions
        )

        cert = x509.load_pem_x509_certificate(cert_pem.encode())
        fingerprint = cert.fingerprint(hashes.SHA256()).hex()

        db_cert = KojiCertificate(
            user_id=request.user_id,
            organization_id=request.organization_id,
            issued_by = current_user.id,
            cert_data=cert_pem,
            private_key=key_pem,
            valid_from=datetime.utcnow(),
            valid_to=datetime.utcnow() + timedelta(days=request.valid_days),
            revoked=False,
            permissions=request.permissions
        )
        
        session.add(db_cert)
        await session.commit()
        await session.refresh(db_cert)
        
        return CertificateResponse(
            id = db_cert.id,
            cert_pem=cert_pem,
            private_key_pem=key_pem,
            fingerprint=fingerprint,
            valid_from=db_cert.valid_from,
            valid_to=db_cert.valid_to
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Certificate generation failed: {str(e)}"
        )
    
    
async def check_cert_permissions(
    current_user: UsersModel,
    target_user_id: int,
    session: AsyncSession
) -> bool:
    if current_user.role == "admin":
        return True

    if current_user.role == "member":
        if current_user.id != target_user_id:
            raise HTTPException(
                status_code=403,
                detail="Пользователи могут запрашивать сертификаты только для себя"
            )
        return True

    if current_user.role == "organizer":
        stmt = select(OrganizationsMembersModel).where(
            OrganizationsMembersModel.member_id == target_user_id,
            OrganizationsMembersModel.organization_id.in_(
                select(OrganizationsModel.id).where(
                    OrganizationsModel.created_by == current_user.id
                )
            )
        )
        result = await session.execute(stmt)
        if not result.scalars().first():
            raise HTTPException(
                status_code=403,
                detail="Может выдавать сертификаты только членам своей организации"
            )
        return True
        
    return False



def get_ca_cert() -> x509.Certificate:
    if _CA_CACHE['cert'] is None:
        with open("certs/ca.crt", "rb") as f:
            _CA_CACHE['cert'] = x509.load_pem_x509_certificate(f.read())
    return _CA_CACHE['cert']

def get_ca_key() -> rsa.RSAPrivateKey:
    if _CA_CACHE['key'] is None:
        with open("certs/ca.key", "rb") as f:
            key_data = f.read()
            try:
                _CA_CACHE['key'] = serialization.load_pem_private_key(
                    key_data,
                    password=None,
                    backend=default_backend()
                )
            except ValueError as e:
                logger.error("Invalid CA key file format")
                raise HTTPException(
                    status_code=500,
                    detail="Invalid CA key format. Regenerate CA materials."
                )
    
    return _CA_CACHE['key']

