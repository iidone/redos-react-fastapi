from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from src.schemas.organizations import OrganizationResponce
from src.models.organizations import OrganizationsModel
from src.services.auth import SessionDep

router = APIRouter(prefix = "/v1/organizations")

@router.post('/organization', response_model = List[OrganizationResponce], tags = ["Организации"], summary=["Все Организации"])
async def get_all_organizations(session: SessionDep):
    try:
        result = await session.execute(select(OrganizationsModel))
        organizations = result.scalars().all()
        return organizations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")