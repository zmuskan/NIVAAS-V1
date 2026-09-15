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

    with get_connection() as conn:

        repository = RecommendationRepository(conn)

        service = RecommendationService(
            repository=repository,
        )

        return service.recommend(
            min_budget=request.min_budget,
            max_budget=request.max_budget,
            work=request.office_locality or "",
            priority=(
                "affordable"
                if request.prioritize_affordability
                else "choices"
            ),
            lifestyle=request.user_type or "",
            bhk=None,
            limit=10,
        )
