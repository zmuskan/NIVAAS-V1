from __future__ import annotations

from backend.app.repositories.recommendation_repository import RecommendationRepository

from backend.app.schemas.locality_recommendation import (
    LocalityRecommendationListResponse,
    LocalityRecommendationResponse,
)


class RecommendationService:

    def __init__(
        self,
        repository: RecommendationRepository,
    ):
        self.repository = repository

    def recommend(
        self,
        budget: float,
        bhk: int | None,
        limit: int,
    ) -> LocalityRecommendationListResponse:

        rows = self.repository.fetch_candidates(budget)

        recommendations = []

        for row in rows:

            avg_rent = float(row["avg_rent"])
            listing_count = int(row["listing_count"])

            score = 0

            # Budget fit

            if avg_rent <= budget:
                score += 60

            else:
                difference = avg_rent - budget

                score += max(
                    0,
                    60 - (difference / budget) * 60,
                )

            # Availability

            score += min(
                listing_count * 2,
                40,
            )

            score = round(
                min(score, 100),
                2,
            )

            recommendations.append(
                LocalityRecommendationResponse(
                    locality=row["locality"],
                    min_rent=float(row["min_rent"]),
                    avg_rent=float(row["avg_rent"]),
                    max_rent=float(row["max_rent"]),
                    listing_count=listing_count,
                    match_reason=(
                        "Fits your budget and offers strong rental availability"
                    ),
                )
            )

        recommendations.sort(
            key=lambda x: x.avg_rent,
        )

        recommendations = recommendations[:limit]

        return LocalityRecommendationListResponse(
            items=recommendations,
            total=len(recommendations),
        )
