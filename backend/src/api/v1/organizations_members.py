from typing_extensions import List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.schemas.organizations_members import OrganizationMemberResponce
from src.models.organizations_members import OrganizationsMembersModel
from src.services.auth import SessionDep

router = APIRouter(prefix = "/v1/organizations_members")

@router.get('/organizations_members', 
            response_model = List[OrganizationMemberResponce], 
            tags = ["Участники"], 
            summary="Все участники")
async def get_all_organizations_members(session: SessionDep):
    try:
        result = await session.execute(select(OrganizationsMembersModel))
        organizations_members = result.scalars().all()
        await session.commit()
        print("Returning members:", organizations_members)
        return organizations_members
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")