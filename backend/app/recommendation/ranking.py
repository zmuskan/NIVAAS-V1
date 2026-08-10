from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def recommend(
    rent_weight: float = 0.4,
    metro_weight: float = 0.3,
    popularity_weight: float = 0.3,
    limit: int = 10,
):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                WITH features AS (
                    SELECT
                        locality_id,

                        MAX(
                            CASE
                                WHEN feature_name='rent_score'
                                THEN feature_value
                            END
                        ) AS rent_score,

                        MAX(
                            CASE
                                WHEN feature_name='metro_score'
                                THEN feature_value
                            END
                        ) AS metro_score,

                        MAX(
                            CASE
                                WHEN feature_name='property_count'
                                THEN feature_value
                            END
                        ) AS property_count

                    FROM feature_store.locality_feature
                    GROUP BY locality_id
                )

                SELECT
                    l.name,

                    ROUND(
                        (
                            COALESCE(f.rent_score,0) * %s
                            +
                            COALESCE(f.metro_score,0) * %s
                            +
                            COALESCE(f.property_count,0) * %s
                        )::numeric,
                        2
                    ) AS recommendation_score

                FROM features f

                JOIN core.locality l
                ON l.locality_id = f.locality_id

                ORDER BY recommendation_score DESC

                LIMIT %s
                """,
                (
                    rent_weight,
                    metro_weight,
                    popularity_weight,
                    limit,
                ),
            )

            return cur.fetchall()


if __name__ == "__main__":

    init_pool()

    try:
        rows = recommend()

        for row in rows:
            print(row)

    finally:
        close_pool()
