"""
Main FastAPI application
Cloud Monitoring System - COMPLETE with ML Features
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.config import settings
from app.database import init_db
from app.routers import auth, metrics, instances, health, ml_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Cloud Monitoring System - ML Enhanced",
    version="2.0.0",
    description="Production-grade cloud monitoring system with 10 ML features for AWS EC2 instances",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting Cloud Monitoring System - ML Enhanced v2.0.0")
    init_db()
    logger.info("Database initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Cloud Monitoring System")


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers - ORIGINAL FEATURES
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(instances.router, prefix="/api")

# Include ML routes - ML FEATURES
app.include_router(ml_routes.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with feature list"""
    return {
        "message": "Cloud Monitoring System API - ML Enhanced",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/api/docs",
        "features": {
            "original": [
                "Real-time CPU/Memory/Disk/Network metrics",
                "Prometheus integration",
                "Alert system with email notifications",
                "Instance management",
                "JWT authentication",
                "Multi-user support"
            ],
            "ml_enhanced": [
                "Anomaly detection (Isolation Forest + One-Class SVM)",
                "CPU usage prediction (Prophet forecasting)",
                "Memory usage forecasting",
                "Memory leak detection",
                "Instance health scoring (0-100)",
                "System failure prediction",
                "Root cause analysis",
                "Capacity planning (14-30 days)",
                "Auto-scaling recommendations",
                "ML dashboard summary"
            ]
        },
        "endpoints": {
            "health": "/api/health",
            "auth": "/api/auth (login, register)",
            "metrics": "/api/metrics (cpu, memory, disk, network)",
            "instances": "/api/instances (CRUD operations)",
            "ml": "/api/ml (10 ML features)",
            "docs": "/api/docs (Swagger UI)"
        }
    }


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Cloud Monitoring System API",
        "version": "2.0.0",
        "documentation": "/api/docs",
        "redoc": "/api/redoc",
        "openapi_schema": "/api/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
