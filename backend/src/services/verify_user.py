from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.orm import aliased
from typing import List
from datetime import datetime
from src.models.users import UsersModel
from src.models.organizations import OrganizationsModel
from src.models.organizations_members import OrganizationsMembersModel
from src.schemas.organizations_members import OrganizationMemberResponse, OrganizationMemberCreate
from src.services.auth import SessionDep


async def verify_user(
    organization_id: int,
    organizer_id: int,
    session: SessionDep
):
    org_member = await session.scalar(
        select(OrganizationsMembersModel).where(
            OrganizationsMembersModel.member_id == organizer_id,
            OrganizationsMembersModel.organization_id == organization_id
        )
    )
    
    if not org_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не является членом этой организации"
        )
    user = await session.scalar(
        select(UsersModel).where(
            UsersModel.id == organizer_id,
            or_(
            UsersModel.role == "organizer",
            UsersModel.role == "admin")
        )
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для добавления участников"
        )
    
    return True
