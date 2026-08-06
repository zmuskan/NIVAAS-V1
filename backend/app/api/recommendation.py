from fastapi import APIRouter, Depends, Query

from backend.app.dependencies import get_db_connection
from backend.app.repositories.recommendation_repository import RecommendationRepository
from backend.app.schemas.recommendation import RecommendationListResponse
from backend.app.services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


def get_service(
    conn=Depends(get_db_connection),
):

    return RecommendationService(
        RecommendationRepository(conn)
    )


@router.get("", response_model=RecommendationListResponse)
def recommend(

    budget: float = Query(..., gt=0),

    bhk: int | None = None,

    limit: int = Query(10, ge=1, le=50),

    service: RecommendationService = Depends(get_service),

):

    return service.recommend(
        budget=budget,
        bhk=bhk,
        limit=limit,
    )
