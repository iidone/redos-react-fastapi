from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from src.database.database import engine, Base
from src.models.users import UsersModel


router = APIRouter(prefix="/v1/database")


@router.post("/setup_db", tags = ["База Данных"], summary=["Инициализация БД"])
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "БД инициализирована"}