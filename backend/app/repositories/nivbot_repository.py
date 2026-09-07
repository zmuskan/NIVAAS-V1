from backend.app.database import get_connection


class NivBotRepository:


    @staticmethod
    def get_locality_context(locality_name: str):

        query = """
        SELECT
            l.name,

            MAX(CASE WHEN lf.feature_name='avg_rent'
                THEN lf.feature_value END) AS avg_rent,

            MAX(CASE WHEN lf.feature_name='listing_count'
                THEN lf.feature_value END) AS listing_count,

            MAX(CASE WHEN lf.feature_name='inventory_score'
                THEN lf.feature_value END) AS inventory_score,

            MAX(CASE WHEN lf.feature_name='density_score'
                THEN lf.feature_value END) AS density_score,

            MAX(CASE WHEN lf.feature_name='overall_score'
                THEN lf.feature_value END) AS overall_score,

            MAX(CASE WHEN lf.feature_name='rent_score'
                THEN lf.feature_value END) AS rent_score

        FROM core.locality l

        LEFT JOIN feature_store.locality_feature lf
            ON l.locality_id = lf.locality_id

        WHERE LOWER(l.name) = LOWER(%s)

        GROUP BY l.name

        LIMIT 1
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (locality_name,))
                return cur.fetchone()
