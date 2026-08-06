from backend.app.repositories.similar_repository import SimilarRepository
from backend.app.schemas.similar import (
    SimilarProperty,
    SimilarPropertyList,
)


class SimilarService:

    def __init__(self, repo):

        self.repo = repo

    def similar(self, property_id, limit):

        target = self.repo.fetch_property(property_id)

        rows = self.repo.fetch_candidates(property_id)

        results = []

        for row in rows:

            score = 0

            score += max(
                0,
                30 - abs(row["bhk"] - target["bhk"]) * 15,
            )

            score += max(
                0,
                30
                - abs(
                    float(row["rent_amount"])
                    - float(target["rent_amount"])
                )
                / float(target["rent_amount"])
                * 30,
            )

            score += max(
                0,
                20
                - abs(
                    float(row["area_sqft"])
                    - float(target["area_sqft"])
                )
                / 100,
            )

            if row["property_type"] == target["property_type"]:

                score += 20

            row["similarity_score"] = round(score, 2)

            results.append(row)

        results.sort(
            key=lambda x: x["similarity_score"],
            reverse=True,
        )

        results = results[:limit]

        return SimilarPropertyList(
            items=[
                SimilarProperty.model_validate(r)
                for r in results
            ],
            total=len(results),
        )
