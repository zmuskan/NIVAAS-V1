from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)

from backend.app.recommendation.explain import (
    generate_reasons,
)


def recommend(
    rent_weight: float = 0.4,
    metro_weight: float = 0.3,
    property_weight: float = 0.3,
):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    l.name,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='rent_score'
                            THEN feature_value
                        END
                    ),0) AS rent_score,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='metro_score'
                            THEN feature_value
                        END
                    ),0) AS metro_score,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='property_count'
                            THEN feature_value
                        END
                    ),0) AS property_count

                FROM feature_store.locality_feature f
                JOIN core.locality l
                    ON l.locality_id = f.locality_id

                GROUP BY l.name
                """
            )

            rows = cur.fetchall()

    scored = []

    for row in rows:

        name = row[0]
        rent_score = float(row[1])
        metro_score = float(row[2])
        property_count = float(row[3])

        score = (
            rent_score * rent_weight
            + metro_score * metro_weight
            + property_count * property_weight
        )

        reasons = generate_reasons(
            rent_score=rent_score,
            metro_score=metro_score,
            property_count=property_count,
        )

        scored.append(
            {
                "locality": name,
                "score": round(score, 2),
                "reasons": reasons,
            }
        )

    scored.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return scored[:10]


if __name__ == "__main__":

    init_pool()

    try:

        rows = recommend(
            rent_weight=0.5,
            metro_weight=0.3,
            property_weight=0.2,
        )

        for row in rows:
            print(row)

    finally:
        close_pool()
