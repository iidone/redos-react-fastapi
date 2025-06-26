from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from src.schemas.organizations import OrganizationResponce, OrganizationCreate
from src.models.users import UsersModel
from src.models.organizations import OrganizationsModel
from src.services.auth import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix = "/v1/organizations")

@router.get('/organizations', 
            response_model = List[OrganizationResponce], 
            tags = ["Организации"], 
            summary=["Все организации"])
async def get_all_organizations(session: SessionDep):
    try:
        result = await session.execute(select(OrganizationsModel))
        organizations = result.scalars().all()
        return organizations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@router.post(
    '/organizations',
    response_model=OrganizationResponce,
    status_code=status.HTTP_201_CREATED,
    tags=["Организации"], 
    summary="Добавить организацию"
)
async def create_organization(  
    session: SessionDep, 
    organization: OrganizationCreate):
    try:
        existing_org = await session.scalar(
            select(OrganizationsModel).where(OrganizationsModel.name == organization.name)
        )
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization already exists"
            )
        user = await session.scalar(
            select(UsersModel).where(UsersModel.id == organization.created_by)
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        new_org = OrganizationsModel(
            name=organization.name,
            description=organization.description,
            created_by=organization.created_by
        )
        
        session.add(new_org)
        await session.commit()
        await session.refresh(new_org)
        return OrganizationResponce.model_validate(new_org)

    except HTTPException:
        raise

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating organization: {str(e)}"
        )
        
        
@router.delete("/{organizations_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Организации"],
    summary="Удалить организацию")
async def delete_organization(
    session: SessionDep,
    organization_id: int = Path(..., title="ID организации", gt=0)
):
    try:
        org = await session.scalar(
            select(OrganizationsModel).where(OrganizationsModel.id == organization_id)
        )
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        has_users = await session.scalar(
            select(UsersModel).where(UsersModel.organization_id == organization_id).limit(1)
        )
        if has_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete organization with attached users"
            )
        await session.delete(org)
        await session.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting organization: {str(e)}"
        )