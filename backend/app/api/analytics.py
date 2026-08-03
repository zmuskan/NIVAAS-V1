from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.dependencies import get_db_connection
from backend.app.repositories.analytics_repository import AnalyticsRepository
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


def get_analytics_service(
    conn=Depends(get_db_connection),
) -> AnalyticsService:

    repository = AnalyticsRepository(conn)

    return AnalyticsService(repository)


@router.get("")
def list_analytics(
    service: AnalyticsService = Depends(get_analytics_service),
):

    return service.list_all()


@router.get("/top-rent")
def top_rent(
    limit: int = Query(default=10, ge=1, le=100),
    service: AnalyticsService = Depends(get_analytics_service),
):

    return service.top_rent(limit)


@router.get("/top-listings")
def top_listings(
    limit: int = Query(default=10, ge=1, le=100),
    service: AnalyticsService = Depends(get_analytics_service),
):

    return service.top_listing_count(limit)


@router.get("/{locality_id}")
def get_locality_analytics(
    locality_id: UUID,
    service: AnalyticsService = Depends(get_analytics_service),
):

    try:

        return service.get_by_locality(locality_id)

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
