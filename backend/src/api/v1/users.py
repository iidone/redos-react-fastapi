from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from src.models.organizations import OrganizationsModel
from src.models.users import UsersModel
from src.schemas.users import DeleteMasterRequest, UsersSchema, UserResponce, UserCreate, UpdateUserRole
from src.services.auth import (
    add_to_blacklist,
    pwd_context, 
    SessionDep,
    oauth2_scheme,
    create_access_token,
    authenticate_user,
    token_blacklist,
    verify_password
)

router = APIRouter(prefix="/v1/users")

@router.post("/login", tags=["Пользователи"],summary = ["Авторизация"])
async def login_user(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "username": user.username,
            "user_id": user.id,
            "role": user.role,
            "user_role": user.role,
            "full_name": user.full_name,
        }
    }

@router.post("/logout", tags=["Пользователи"], summary=["Выход"])
async def logout_user(
    session: SessionDep,
    response: Response,
    token: str = Depends(oauth2_scheme),
):
    try:
        await add_to_blacklist(token)

        response.delete_cookie("access_token")
        
        return {
            "message": "Logout successful",
            "detail": "Token invalidated. Client should discard the token."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout error: {str(e)}"
        )
    



@router.post("/users", response_model=UserCreate, status_code=status.HTTP_201_CREATED, tags=["Пользователи"], summary=["Добавить пользователя"])
async def add_user(user_data: UsersSchema, session: SessionDep):
    try:
        existing_user = await session.execute(
            select(UsersModel).where(UsersModel.username == user_data.username)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exist."
            )
        new_user = UsersModel(
            role=user_data.role,
            username=user_data.username,
            full_name=user_data.full_name,
            password=pwd_context.hash(user_data.password),
            email=user_data.email,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        return new_user
    
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )




@router.get("/users", response_model=List[UserResponce], tags=["Пользователи"], summary=["Получить всех пользователей"])
async def get_all_users(session: SessionDep):
    try:
        result = await session.execute(select(UsersModel))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    
    
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags = ["Пользователи"],
    summary="Удалить пользователя",
    responses={
        204: {"description": "Пользователь успешно удален"},
        404: {"description": "Пользователь не найден"},
        400: {"description": "Невозможно удалить пользователя (есть связанные данные)"},
        422: {"description": "Ошибка валидации параметров"}
    }
)
async def delete_user(
    session: SessionDep,
    user_id: int = Path(title="ID пользователя", gt=0, example=1),
):
    try:
        user = await session.scalar(
            select(UsersModel).where(UsersModel.id == user_id)
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        has_organizations = await session.scalar(
            select(OrganizationsModel)
            .where(OrganizationsModel.created_by == user_id)
            .limit(1)
        )
        
        if has_organizations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Невозможно удалить пользователя: у него есть созданные организации"
            )

        await session.execute(
            delete(UsersModel).where(UsersModel.id == user_id)
        )
        await session.commit()
        return None

    except HTTPException:
        raise
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении пользователя: {str(e)}"
        )
        
        
@router.patch('/{user_id}/role',
            response_model = UsersSchema,
            tags = ["Пользователи"],
            summary="Обновить роль пользователя")
async def update_user_role(
    user_id: int,
    role_update: UpdateUserRole,
    session: SessionDep
):
    try:
        user = await session.execute(
            select(UsersModel)
            .where(UsersModel.id == user_id)
        )
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка не найдена"
            )
        user.role = role_update.role
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении роли пользователя: {str(e)}"
            )