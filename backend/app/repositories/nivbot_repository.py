from backend.app.database import get_connection


class NivBotRepository:

    @staticmethod
    def get_locality_context(locality_name: str):

        query = """
        SELECT
            l.name,
            lf.overall_score,
            lf.inventory_score,
            lf.density_score,
            l.avg_rent,
            l.property_count
        FROM feature_store.locality_feature lf
        JOIN core.locality l
            ON l.locality_id = lf.locality_id
        WHERE LOWER(l.name)=LOWER(%s)
        LIMIT 1
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (locality_name,))
                return cur.fetchone()
