from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete
from src.models.users import UsersModel
from src.schemas.users import DeleteMasterRequest, UsersSchema, UserResponce, UserCreate
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
            "user_role": user.role,
            "first_name": user.first_name,
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
    



@router.post("/add_user", response_model=UserCreate, status_code=status.HTTP_201_CREATED, tags=["Пользователи"], summary=["Добавить пользователя"])
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
            first_name=user_data.first_name,
            last_name=user_data.last_name,
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




@router.get("/all_user", response_model=List[UserResponce], tags=["Пользователи"], summary=["Получить всех пользователей"])
async def get_all_users(session: SessionDep):
    try:
        result = await session.execute(select(UsersModel))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")