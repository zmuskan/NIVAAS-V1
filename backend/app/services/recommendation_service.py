from __future__ import annotations

from backend.app.repositories.recommendation_repository import (
    RecommendationRepository,
)

from backend.app.schemas.locality_recommendation import (
    LocalityRecommendationListResponse,
    LocalityRecommendationResponse,
)

from backend.app.services.similarity_service import (
    get_similarity,
)
WORK_CLUSTERS = {

    "whitefield": [
        "Whitefield",
        "Whitefield Hope Farm Junction",
        "Kadugodi",
        "Mahadevapura",
        "Krishnarajapura",
        "Brookefield",
        "Itpl",
    ],

    "electronic_city": [
        "Electronics City",
        "Electronic City Phase 1",
    ],

    "koramangala": [
        "Koramangala",
        "Hsr Layout",
        "Btm Layout",
    ],

    "hebbal": [
        "Hebbal",
        "Nagawara",
        "Hbr Layout",
        "Thanisandra",
    ]
}

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
        print("TOTAL ROWS FROM DB:", len(rows))

        if rows:
            print("FIRST ROW:")
            print(rows[0])

        scored_items = []

        for row in rows:

            locality = row["locality"]
            commute_bonus = 0

            work_key = work.lower().replace(" ", "_")

            if work_key in WORK_CLUSTERS:

                if locality in WORK_CLUSTERS[work_key]:

                    commute_bonus = 15

            avg_rent = float(row["avg_rent"])

            listing_count = int(row["listing_count"])
            print(locality, listing_count)

            if listing_count < 3:
                continue

            final_base_score = float(
                row.get("final_score") or 0
            )

            student_score = float(
                row.get("student_score") or 0
            )

            family_score = float(
                row.get("family_score") or 0
            )

            inventory_score = float(
                row.get("inventory_score") or 0
            )

            density_score = float(
                row.get("density_score") or 0
            )

            rent_score = float(
                row.get("rent_score") or 0
            )

            #################################################
            # Normalization
            #################################################

            final_base_score = min(
                final_base_score,
                100,
            )

            student_score = min(
                student_score,
                100,
            )

            family_score = min(
                family_score,
                100,
            )

            inventory_score = min(
                inventory_score,
                100,
            )

            density_score = min(
                density_score,
                100,
            )

            rent_score = min(
                rent_score,
                100,
            )

            #################################################
            # Affordability Score
            #################################################

            mid_budget = (
                min_budget + max_budget
            ) / 2

            affordability_score = max(
                0,
                100
                - (
                    abs(
                        avg_rent - mid_budget
                    )
                    / mid_budget
                )
                * 100,
            )

            #################################################
            # Lifestyle Score
            #################################################

            lifestyle_score = 50

            if (
                lifestyle
                and lifestyle.lower() == "student"
            ):
                lifestyle_score = student_score
                reason = "Strong student-friendly locality"

            elif (
                lifestyle
                and lifestyle.lower() == "family"
            ):
                lifestyle_score = family_score
                reason = "Good family-friendly locality"

            elif (
                lifestyle
                and lifestyle.lower() == "couple"
            ):
                lifestyle_score = (
                    family_score * 0.5
                    + density_score * 0.5
                )
                reason = "Balanced lifestyle for couples"

            elif (
                lifestyle
                and lifestyle.lower()
                in ["young professional", "professional"]
            ):
                lifestyle_score = (
                    density_score * 0.60
                    + inventory_score * 0.40
                )
                reason = "Popular among working professionals"

            #################################################
            # Priority Score
            #################################################

            priority_score = 50

            if priority == "affordable":
                priority_score = (
                    rent_score
                )

            elif priority == "choices":
                priority_score = (
                    inventory_score
                )

            elif priority == "active":
                priority_score = (
                    density_score
                )

            elif priority == "quiet":
                priority_score = (
                    100
                    - density_score
                )

            #################################################
            # Final Score
            #################################################

            final_score = round(
            (
               final_base_score * 0.50
               + lifestyle_score * 0.10
               + priority_score * 0.15
               + affordability_score * 0.15
               + inventory_score * 0.10
            )
            + commute_bonus,
            2,
            )
            final_score = max(0, min(final_score, 100))


            user_vector = [
                lifestyle_score,
                affordability_score,
                priority_score,
            ]

            locality_vector = [
                student_score,
                rent_score,
                inventory_score,
            ]

            similarity_score = (
                get_similarity(
                    user_vector,
                    locality_vector,
                )
            )

            final_score = round(
                final_score * 0.70
                + similarity_score * 100 * 0.05,
                2,
            )

            final_score = max(
                0,
                min(final_score, 100),
            )

            #################################################
            # Explanation
            #################################################

            reason = "Balanced Recommendation"

            if commute_bonus > 0:
                reason = "Near Work Location"

            elif affordability_score >= 80:
                reason = "Budget Friendly"

            elif inventory_score >= 60:
                reason = "High Availability"

            elif density_score >= 70:
                reason = "Active Lifestyle Area"
            print(
                locality,
                "base=",
                round(
                    final_base_score,
                    2,
                ),
                "lifestyle=",
                round(
                    lifestyle_score,
                    2,
                ),
                "priority=",
                round(
                    priority_score,
                    2,
                ),
                "final=",
                round(
                    final_score,
                    2,
                ),

            )
            highlights = []



            if commute_bonus > 0:
                highlights.append("Near Work Location")

            if affordability_score >= 80:
                highlights.append("Budget Friendly")

            if inventory_score >= 60:
                highlights.append("High Availability")

            if density_score >= 70:
                highlights.append("Active Lifestyle Area")

            if lifestyle.lower() == "student":
                highlights.append("Student Friendly")

            elif lifestyle.lower() == "family":
                highlights.append("Family Friendly")

            if highlights:
                reason = ", ".join(highlights)
            else:
                reason = "Balanced Recommendation"

            scored_items.append(
                {
                    "score": final_score,
                    "item": LocalityRecommendationResponse(
                        locality=locality,
                        min_rent=float(row["min_rent"]),
                        avg_rent=float(row["avg_rent"]),
                        max_rent=float(row["max_rent"]),
                        listing_count=listing_count,

                        inventory_score=round(
                            inventory_score,
                            2,
                        ),

                        density_score=round(
                            density_score,
                            2,
                        ),

                        final_score=round(
                            final_score,
                            2,
                        ),

                        student_score=round(
                            student_score,
                            2,
                        ),

                        family_score=round(
                            family_score,
                            2,
                        ),

                        rent_score=round(
                            rent_score,
                            2,
                        ),

                        similarity_score=round(
                            similarity_score * 100,
                            2,
                        ),

                        affordability_score=round(
                            affordability_score,
                            2,
                        ),

                        commute_bonus=commute_bonus,

                        match_reason=reason,
                    ),
                }
            )

            print("APPENDED:", locality)

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


