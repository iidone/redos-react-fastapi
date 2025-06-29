from datetime import datetime
from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete, func
from src.schemas.organizations import OrganizationResponse, OrganizationCreate
from src.models.users import UsersModel
from src.models.organizations import OrganizationsModel
from src.services.auth import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix = "/v1/organizations")

@router.get('/organizations', 
            response_model = List[OrganizationResponse], 
            tags = ["Организации"], 
            summary=["Все организации"])
async def get_all_organizations(session: SessionDep):
    try:
        result = await session.execute(select(OrganizationsModel))
        organizations = result.scalars().all()
        await session.commit()
        return organizations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

@router.post(
    '/organizations',
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Организации"], 
    summary="Добавить организацию"
)
async def create_organization(  
    session: SessionDep, 
    organization: OrganizationCreate
):
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
            created_by=organization.created_by,
            created_at=func.now()
        )
        
        session.add(new_org)
        await session.flush()

        org_from_db = await session.scalar(
            select(OrganizationsModel).where(OrganizationsModel.id == new_org.id)
        )
        
        if not org_from_db:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created organization"
            )
            
        await session.commit()
        
        return {
            "id": org_from_db.id,
            "name": org_from_db.name,
            "description": org_from_db.description,
            "created_by": org_from_db.created_by,
            "created_at": datetime.utcnow()
        }

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
                detail="Организация не найдена"
            )
        has_users = await session.scalar(
            select(UsersModel).where(UsersModel.organization_id == organization_id).limit(1)
        )
        if has_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невозможно удалить организацию: в ней есть участники"
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
            detail=f"Ошибка удаления: {str(e)}"
        )