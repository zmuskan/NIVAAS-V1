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
    min_budget: float,
    max_budget: float,
        work: str,
        priority: str,
        lifestyle: str,
        bhk: int | None,
        limit: int,
    ) -> LocalityRecommendationListResponse:

        rows = self.repository.fetch_candidates(
            min_budget,
            max_budget,
        )
        print("BUDGET RECEIVED:", min_budget, max_budget)

        for row in rows[:10]:
            print(
                row["locality"],
                row["avg_rent"]
            )

        shortlisted = []

        #################################################
        # FILTER STAGE
        #################################################

        shortlisted = rows

        #################################################
        # SCORING STAGE
        #################################################

        scored_items = []

        for row in shortlisted:

            locality = row["locality"]

            avg_rent = float(row["avg_rent"])

            listing_count = int(row["listing_count"])

            #############################################
            # Affordability Score
            #############################################

            mid_budget = (min_budget + max_budget) / 2

            affordability_score = max(
                0,
                100 - (avg_rent / mid_budget) * 100,
            )
            #############################################
            # Availability Score
            #############################################

            availability_score = min(
                listing_count * 5,
                100,
            )

            #############################################
            # Workplace Score
            #############################################

            workplace_score = 50

            #############################################
            # Lifestyle Score
            #############################################

            lifestyle_score = 50
            #############################################
            # Final Score
            #############################################

            final_score = round(
                (
                    affordability_score * 0.60
                    + availability_score * 0.20
                    + workplace_score * 0.20
                ),
                2,
            )

            #############################################
            # Reason
            #############################################

            if workplace_score == 100:
                reason = "Near workplace"

            elif affordability_score > 70:
                reason = "Affordable option"

            elif availability_score > 60:
                reason = "High availability"

            else:
                reason = "Balanced option"

            scored_items.append(
                {
                    "score": final_score,
                    "item": LocalityRecommendationResponse(
                        locality=locality,
                        min_rent=float(row["min_rent"]),
                        avg_rent=float(row["avg_rent"]),
                        max_rent=float(row["max_rent"]),
                        listing_count=listing_count,
                        match_reason=reason,
                    ),
                }
            )

        #################################################
        # SORT
        #################################################

        scored_items.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        recommendations = [
            item["item"]
            for item in scored_items[:limit]
        ]

        return LocalityRecommendationListResponse(
            items=recommendations,
            total=len(recommendations),
        )
