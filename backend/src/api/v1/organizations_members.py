from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_, delete
from sqlalchemy.orm import aliased
from typing import List
from datetime import datetime
from src.models.users import UsersModel
from src.models.organizations import OrganizationsModel
from src.models.organizations_members import OrganizationsMembersModel
from src.schemas.organizations_members import OrganizationMemberResponse, OrganizationMemberCreate
from src.services.auth import SessionDep
from src.services.VerifyUser import verify_user

router = APIRouter(prefix = "/v1/organizations_members", tags = ["Участники"])


@router.get("/", response_model=List[OrganizationMemberResponse], summary= "Получить всех участников")
async def get_members(session: SessionDep):
    try:
        MemberUser = aliased(UsersModel)
        OrganizerUser = aliased(UsersModel)
        
        query = (
            select(
                OrganizationsMembersModel.member_id,
                MemberUser.full_name.label("member_name"),
                OrganizationsMembersModel.organization_id,
                OrganizationsModel.name.label("organization_name"),
                OrganizationsMembersModel.organizer_id,
                OrganizerUser.full_name.label("organizer_name"),
                OrganizationsMembersModel.assigned_at,
                OrganizationsMembersModel.id
            )
            .select_from(OrganizationsMembersModel)
            .join(MemberUser, MemberUser.id == OrganizationsMembersModel.member_id)
            .join(OrganizationsModel, OrganizationsModel.id == OrganizationsMembersModel.organization_id)
            .join(OrganizerUser, OrganizerUser.id == OrganizationsMembersModel.organizer_id)
        )
        
        result = await session.execute(query)
        return result.mappings().all()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении списка участников: {str(e)}"
        )
        
        
@router.post("/",
            status_code=status.HTTP_201_CREATED,
            summary= "Добавить участника в организацию")
async def add_member(session: SessionDep, member_data: OrganizationMemberCreate):
    try:
        await verify_user(
            organization_id=member_data.organization_id,
            organizer_id=member_data.organizer_id,
            session=session
        )
        member = await session.scalar(
            select(UsersModel).where(UsersModel.id == member_data.member_id)
        )
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        organization = await session.scalar(
            select(OrganizationsModel).where(OrganizationsModel.id == member_data.organization_id)
        )
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Организация не найдена"
            )
        existing_member = await session.scalar(
            select(OrganizationsMembersModel).where(
                OrganizationsMembersModel.member_id == member_data.member_id,
                OrganizationsMembersModel.organization_id == member_data.organization_id
            )
        )
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже является участником этой организации"
            )
        new_member = OrganizationsMembersModel(
            member_id=member_data.member_id,
            organization_id=member_data.organization_id,
            organizer_id=member_data.organizer_id,
            assigned_at=datetime.utcnow()
        )

        session.add(new_member)
        await session.commit()
        await session.refresh(new_member)

        return {
            "message": "Пользователь успешно добавлен в организацию",
            "member_id": new_member.member_id,
            "organization_id": new_member.organization_id
        }
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении участника: {str(e)}"
        )
        
        
@router.delete(
    "/{organization_id}/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary = "Удалить участника"
    )
async def delete_member(
    organization_id: int,
    member_id: int,
    session: SessionDep
):
    try:
        exists = await session.scalar(
            select(OrganizationsMembersModel).where(
                OrganizationsMembersModel.member_id == member_id,
                OrganizationsMembersModel.organization_id == organization_id
            ))
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Участник не найден в указанной организации"
            )
        await session.execute(
            delete(OrganizationsMembersModel).where(
                OrganizationsMembersModel.member_id == member_id,
                OrganizationsMembersModel.organization_id == organization_id
            )
        )
        await session.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении участника: {str(e)}"
        )