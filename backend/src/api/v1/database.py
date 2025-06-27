from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from src.database.database import engine, Base, get_session
from sqlalchemy.orm import Session
from sqlalchemy import String
from src.models.users import UsersModel
from src.models.certificates import CertificatesModel
from src.models.certificates_requests import CertificatesRequestsModel
from src.models.organizations import OrganizationsModel
from src.models.organizations_members import OrganizationsMembersModel
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from src.models import get_model, table_configs
from datetime import datetime
from typing import Dict, Any


router = APIRouter(prefix="/v1/database")
faker = Faker()


@router.post("/setup_db", tags = ["База данных"], summary=["Инициализация БД"])
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "БД инициализирована"}


@router.post("/add_records", tags=["База данных"], summary=["Добавить записи"])
async def add_records(
    table_name: str,
    count: int = 20,
    session: AsyncSession = Depends(get_session)
):
    if not 1 <= count <= 100:
        raise HTTPException(400, "Количество должно быть от 1 до 100")
    
    if table_name not in table_configs:
        available_tables = list(table_configs.keys())
        raise HTTPException(404, f"Доступные таблицы: {', '.join(available_tables)}")

    try:
        Model = get_model(table_name)
        generated_data = []
        
        for _ in range(count):
            item_data: Dict[str, Any] = {}
            for col_name, column in table_configs[table_name]["columns"].items():
                if col_name == "id":
                    continue
                if hasattr(column.type, "__visit_name__"):
                    col_type = column.type.__visit_name__
                else:
                    col_type = str(column.type)
                
                if "str" in col_type.lower() or "text" in col_type.lower():
                    if "email" in col_name.lower():
                        item_data[col_name] = faker.email()
                    elif "full_name" in col_name.lower():
                        item_data[col_name] = faker.name()
                    elif "role" in col_name.lower():
                        item_data[col_name] = "member"
                    elif "status" in col_name.lower():
                        item_data[col_name] = "pending"
                    else:
                        item_data[col_name] = faker.word().capitalize()
                elif "int" in col_type.lower():
                    item_data[col_name] = faker.random_int(1, 100)
                elif "datetime" in col_type.lower():
                    item_data[col_name] = datetime.now()
                elif "boolean" in col_type.lower():
                    item_data[col_name] = faker.boolean()
            valid_data = {
                str(key): value 
                for key, value in item_data.items()
                if hasattr(Model, key)
            }
            
            db_item = Model(**valid_data)
            session.add(db_item)
            generated_data.append(valid_data)
        
        await session.commit()
        
        return {
            "status": "success",
            "generated": len(generated_data),
            "first_record": generated_data[0] if generated_data else None
        }
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, f"Ошибка: {str(e)}")
    finally:
        await session.close()
                