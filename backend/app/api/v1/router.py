from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.opportunities import router as opportunities_router
from app.api.v1.endpoints.misc import (
    tags_router, applications_router, favorites_router, users_router, companies_router
)

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(opportunities_router)
api_router.include_router(tags_router)
api_router.include_router(applications_router)
api_router.include_router(favorites_router)
api_router.include_router(users_router)
api_router.include_router(companies_router)
