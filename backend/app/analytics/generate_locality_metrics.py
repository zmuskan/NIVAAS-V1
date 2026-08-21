from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_metrics():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                TRUNCATE analytics.locality_metrics;
            """)

            cur.execute(
                """
                INSERT INTO analytics.locality_metrics
                (
                    locality_id,
                    listing_count,
                    avg_rent,
                    min_rent,
                    max_rent
                )

                SELECT

                    lm.locality_id,

                    COUNT(l.listing_id),

                    AVG(l.rent_amount),

                    MIN(l.rent_amount),

                    MAX(l.rent_amount)

                FROM analytics.locality_mapping lm

                JOIN core.property p
                    ON p.locality_id = lm.locality_id

                JOIN core.listing l
                    ON l.property_id = p.property_id

                GROUP BY lm.locality_id
                """
            )

            conn.commit()

            print("metrics generated")


if __name__ == "__main__":

    init_pool()

    try:
        generate_metrics()

    finally:
        close_pool()
