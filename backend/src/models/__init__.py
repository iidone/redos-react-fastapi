from sqlalchemy import Column, Integer, String, DateTime
from src.database.database import Base

table_configs = {
    "users": {
        "columns": {
            "id": Column(Integer, primary_key=True),
            "role": Column(String(50)),
            "username": Column(String(50)),
            "first_name": Column(String(50)),
            "last_name": Column(String(50)),
            "password": Column(String(50)),
            "email": Column(String(50)),
        }
    },
    "organizations": {
        "columns": {
            "id": Column(Integer, primary_key=True),
            "name": Column(String(50)),
            "description": Column(String(200)),
            "created_by": Column(Integer),
            "created_at": Column(DateTime),
        }
    }
        
}

def get_model(table_name: str):
    if table_name not in table_configs:
        raise ValueError(f"Таблица {table_name} не найдена")
    
    columns = table_configs[table_name]["columns"]
    
    attrs = {
        '__tablename__': table_name,
        '__table_args__': {'extend_existing': True},
        **columns
    }
    
    return type(f'Dynamic{table_name.capitalize()}', (Base,), attrs)