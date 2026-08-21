from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.dependencies import get_db_connection
from backend.app.repositories.property_repository import PropertyRepository
from backend.app.schemas.property import (
    PropertyListResponse,
    PropertyResponse,
)
from backend.app.services.property_service import PropertyService

router = APIRouter(
    prefix="/properties",
    tags=["Properties"],
)


def get_property_service(
    conn=Depends(get_db_connection),
) -> PropertyService:

    return PropertyService(PropertyRepository(conn))


@router.get("")
def list_properties(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: PropertyService = Depends(get_property_service),
):

    return service.list_properties(limit, offset)


@router.get("/search")
def search_properties(
    min_rent: float | None = None,
    max_rent: float | None = None,
    bhk: int | None = None,
    service: PropertyService = Depends(get_property_service),
):

    return service.search(
        min_rent=min_rent,
        max_rent=max_rent,
        bhk=bhk,
    )


@router.get("/recommendations", response_model=PropertyListResponse)
def get_recommendations(
    budget: float = Query(..., gt=0),
    bhk: int | None = Query(default=None, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: PropertyService = Depends(get_property_service),
) -> PropertyListResponse:
    return service.get_recommendations(
        budget=budget,
        bhk=bhk,
        limit=limit,
    )


@router.get("/locality/{locality_id}")
def properties_by_locality(
    locality_id: UUID,
    service: PropertyService = Depends(get_property_service),
):

    return service.properties_by_locality(locality_id)


@router.get("/{property_id}")
def get_property(
    property_id: UUID,
    service: PropertyService = Depends(get_property_service),
):

    try:
        return service.get_property(property_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
