from backend.app.database import get_connection


def get_locality_profile(locality_name: str):

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    l.name,
                    lm.min_rent,
                    lm.avg_rent,
                    lm.max_rent,
                    lm.listing_count,
                    lm.property_count

                FROM analytics.locality_metrics lm
                JOIN core.locality l
                    ON l.locality_id = lm.locality_id

                WHERE LOWER(l.name)=LOWER(%s)
                """,
                (locality_name,),
            )

            return cur.fetchone()
