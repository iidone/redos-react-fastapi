from sqlalchemy import select
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

SessionDep = Annotated[AsyncSession, Depends(get_session)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

token_blacklist = {}