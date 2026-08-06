from __future__ import annotations

from backend.app.repositories.recommendation_repository import RecommendationRepository
from backend.app.schemas.recommendation import (
    RecommendationListResponse,
    RecommendationResponse,
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
    ) -> RecommendationListResponse:

        rows = self.repository.fetch_candidates(budget)

        recommendations = []

        for row in rows:

            score = 0.0

            #############################
            # Budget
            #############################

            budget_difference = abs(
                float(row["rent_amount"]) - budget
            )

            budget_score = max(
                0,
                35 - (budget_difference / budget) * 35,
            )

            score += budget_score

            #############################
            # BHK
            #############################

            if bhk is not None:

                bhk_difference = abs(
                    row["bhk"] - bhk
                )

                score += max(
                    0,
                    25 - bhk_difference * 10,
                )

            #############################
            # Area
            #############################

            area_score = min(
                float(row["area_sqft"]) / 120,
                15,
            )

            score += area_score

            #############################
            # Furnishing
            #############################

            status = (
                row["furnishing_status"] or ""
            ).upper()

            if "FURNISHED" in status:

                score += 10

            elif "SEMI" in status:

                score += 6

            #############################
            # Property Type
            #############################

            ptype = (
                row["property_type"] or ""
            ).upper()

            if "APARTMENT" in ptype:

                score += 10

            elif "HOUSE" in ptype:

                score += 7

            elif "VILLA" in ptype:

                score += 9

            #############################
            # Locality Popularity
            #############################

            count = row.get("listing_count")

            if count:

                score += min(
                    count / 8,
                    10,
                )

            #############################
            # Rent Efficiency
            #############################

            avg = row.get("avg_rent")

            if avg:

                if float(row["rent_amount"]) <= float(avg):

                    score += 8

            #############################
            # Reserved
            #############################

            ml_score = 0

            score += ml_score

            row["recommendation_score"] = round(score, 2)

            recommendations.append(row)

        recommendations.sort(
            key=lambda x: x["recommendation_score"],
            reverse=True,
        )

        recommendations = recommendations[:limit]

        return RecommendationListResponse(
            items=[
                RecommendationResponse.model_validate(r)
                for r in recommendations
            ],
            total=len(recommendations),
        )
