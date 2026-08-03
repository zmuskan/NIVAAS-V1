from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.dependencies import get_db_connection
from backend.app.repositories.locality_repository import LocalityRepository
from backend.app.services.locality_service import LocalityService

router = APIRouter(
    prefix="/localities",
    tags=["Localities"],
)


def get_locality_service(
    conn=Depends(get_db_connection),
) -> LocalityService:

    repository = LocalityRepository(conn)

    return LocalityService(repository)


@router.get("")
def list_localities(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    service: LocalityService = Depends(get_locality_service),
):

    return service.list_localities(
        limit=limit,
        offset=offset,
    )


@router.get("/{locality_id}")
def get_locality(
    locality_id: UUID,
    service: LocalityService = Depends(get_locality_service),
):

    try:

        return service.get_locality(locality_id)

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
