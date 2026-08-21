from uuid import UUID

from fastapi import APIRouter, Depends, Query

from backend.app.dependencies import get_db_connection
from backend.app.repositories.similar_repository import SimilarRepository
from backend.app.services.similar_service import SimilarService

router = APIRouter(
    prefix="/similar",
    tags=["Similar Properties"],
)


def get_service(
    conn=Depends(get_db_connection),
):

    return SimilarService(
        SimilarRepository(conn)
    )


@router.get("/{property_id}")
def similar(

    property_id: UUID,

    limit: int = Query(
        10,
        ge=1,
        le=50,
    ),

    service: SimilarService = Depends(get_service),

):

    return service.similar(
        property_id,
        limit,
    )
