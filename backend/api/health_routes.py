from fastapi import APIRouter
from services.health_service import HealthService

router = APIRouter(tags=["health"])
health_service = HealthService()

@router.get("/health")
async def health_check():
    return await health_service.check_health()

@router.get("/hello")
async def hello():
    return await health_service.get_hello()
