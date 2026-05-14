"""
JIAPI - Justice & Income API
Vercel Production Ready
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import time

from app.core.config import settings
from app.routers import (
    post2023, pre2023, caselaw, search, 
    amendments, dtaa, sros, circulars,
    auth, admin, health
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Commercial-Grade Bangladesh Tax Law Database API.

    ## Features
    - **Post-2023 API**: Income Tax Act 2023, Rules 2024, Finance Acts
    - **Pre-2023 API**: ITO 1984 with all amendments
    - **Case Law API**: AD, HCD, TAT judgments
    - **Amendment Engine**: Point-in-time queries, diff views
    - **Full-Text Search**: Bengali + English
    - **DTAA Database**: 35+ treaties
    - **Webhook Alerts**: Real-time law change notifications

    ## Authentication
    All endpoints require API key or JWT token.

    ## Rate Limits
    - Free: 100 req/day
    - Basic: 1,000 req/day
    - Professional: 10,000 req/day
    - Enterprise: Unlimited
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel handles CORS at edge
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-API-Version"] = settings.APP_VERSION
    return response


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# Include routers
app.include_router(post2023.router, prefix=settings.API_POST2023_STR, tags=["Post-2023 Legislation"])
app.include_router(pre2023.router, prefix=settings.API_PRE2023_STR, tags=["Pre-2023 Legislation"])
app.include_router(caselaw.router, prefix=settings.API_CASELAW_STR, tags=["Case Law"])
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["Search"])
app.include_router(amendments.router, prefix=settings.API_V1_STR, tags=["Amendments"])
app.include_router(dtaa.router, prefix=settings.API_V1_STR, tags=["DTAA"])
app.include_router(sros.router, prefix=settings.API_V1_STR, tags=["SROs"])
app.include_router(circulars.router, prefix=settings.API_V1_STR, tags=["Circulars"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(health.router, prefix="/health", tags=["Health"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "environment": "production",
        "endpoints": {
            "post2023": f"{settings.API_POST2023_STR}",
            "pre2023": f"{settings.API_PRE2023_STR}",
            "caselaw": f"{settings.API_CASELAW_STR}",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/api/v1")
async def api_info():
    return {
        "api_version": "v1",
        "base_url": settings.API_V1_STR,
        "available_apis": [
            {"name": "Post-2023 Legislation", "path": settings.API_POST2023_STR},
            {"name": "Pre-2023 Legislation", "path": settings.API_PRE2023_STR},
            {"name": "Case Law", "path": settings.API_CASELAW_STR},
            {"name": "Search", "path": f"{settings.API_V1_STR}/search"},
            {"name": "Amendments", "path": f"{settings.API_V1_STR}/amendments"},
            {"name": "DTAA", "path": f"{settings.API_V1_STR}/dtaa"},
            {"name": "SROs", "path": f"{settings.API_V1_STR}/sros"},
            {"name": "Circulars", "path": f"{settings.API_V1_STR}/circulars"},
        ],
        "documentation": "/docs",
        "authentication": "Bearer JWT or API Key"
    }
