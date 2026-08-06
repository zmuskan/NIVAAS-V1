from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.database import check_connection, close_pool, init_pool
from backend.app.api.locality import router as locality_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.property import router as property_router
from backend.app.api.recommendation import router as recommendation_router
from backend.app.api.similar import router as similar_router

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting NIVAAS Backend...")

    init_pool()

    yield

    logger.info("Shutting down NIVAAS Backend...")

    close_pool()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "message": "Welcome to NIVAAS Backend"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "database": check_connection(),
    }


# -----------------------------------------------------
# Routers
# -----------------------------------------------------
#
app.include_router(locality_router)

app.include_router(analytics_router)

app.include_router(property_router)

app.include_router(recommendation_router)

app.include_router(similar_router)
# -----------------------------------------------------
