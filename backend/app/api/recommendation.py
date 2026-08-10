from fastapi import APIRouter

from backend.app.schemas.recommendation_request import (
    RecommendationRequest,
)

from backend.app.recommendation.weighted_ranking import (
    recommend,
)

router = APIRouter(
    prefix="/recommend",
    tags=["recommendation"],
)


@router.post("")
def get_recommendations(
    request: RecommendationRequest,
):

    rows = recommend(
        rent_weight=request.rent_weight,
        metro_weight=request.metro_weight,
        property_weight=request.property_weight,
    )

    return {
        "recommendations": rows
    }
