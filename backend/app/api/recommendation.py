from fastapi import APIRouter

from backend.app.database import get_connection

from backend.app.repositories.recommendation_repository import (
    RecommendationRepository,
)

from backend.app.services.recommendation_service import (
    RecommendationService,
)

from backend.app.schemas.recommendation_request import (
    RecommendationRequest,
)

router = APIRouter(
    prefix="/recommend",
    tags=["recommendation"],
)


@router.post("")
def get_recommendations(
    request: RecommendationRequest,
):

    budget_map = {
        "Below 15k": 15000,
        "15k-25k": 25000,
        "25k-40k": 40000,
        "40k+": 100000,
    }

    budget = budget_map.get(
        request.budget,
        25000,
    )

    with get_connection() as conn:

        repository = RecommendationRepository(conn)

        service = RecommendationService(
            repository=repository,
        )

        result = service.recommend(
            budget=budget,
            bhk=None,
            limit=10,
        )

        return result
