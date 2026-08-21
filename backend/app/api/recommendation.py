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
        "under15": (0, 15000),
        "15to25": (15000, 25000),
        "25to40": (25000, 40000),
        "40to60": (40000, 60000),
        "60plus": (60000, 100000),
    }

    min_budget, max_budget = budget_map.get(
        request.budget,
        (15000, 25000),
    )

    with get_connection() as conn:

        repository = RecommendationRepository(conn)

        service = RecommendationService(
            repository=repository,
        )

        return service.recommend(
            min_budget=min_budget,
            max_budget=max_budget,
            work=request.work,
            priority=request.priority,
            lifestyle=request.lifestyle,
            bhk=None,
            limit=10,
        )
