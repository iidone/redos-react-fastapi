from fastapi import APIRouter
from src.api.v1.users import router as users_router
from src.api.v1.organizations import router as organizations_router
from src.api.v1.database import router as db_router
from src.api.v1.organizations_members import router as organizations_members_router
from src.api.v1.certificates import router as cert_router


main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(db_router)
main_router.include_router(organizations_router)
main_router.include_router(organizations_members_router)
main_router.include_router(cert_router)
