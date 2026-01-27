"""
Health check routes
"""
from fastapi import APIRouter
from datetime import datetime
from app.config import settings
from app.services.prometheus import prometheus_client

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.APP_VERSION,
        "app": settings.APP_NAME
    }


@router.get("/services")
async def check_services():
    """Check health of all services"""
    services = {
        "api": "healthy",
        "prometheus": "healthy" if prometheus_client.check_health() else "unhealthy",
    }
    
    all_healthy = all(status == "healthy" for status in services.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "timestamp": datetime.utcnow(),
        "services": services
    }
