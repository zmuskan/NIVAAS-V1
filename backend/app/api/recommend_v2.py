from fastapi import APIRouter
from backend.app.database import get_connection

router = APIRouter(
    prefix="/recommend",
    tags=["recommend"],
)

@router.get("")
def recommend():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    l.name,

                    MAX(
                        CASE
                            WHEN f.feature_name='final_score'
                            THEN f.feature_value
                        END
                    ) as score

                FROM core.locality l

                JOIN feature_store.locality_feature f
                    ON l.locality_id=f.locality_id

                GROUP BY l.name

                ORDER BY score DESC

                LIMIT 10;
            """)

            rows = cur.fetchall()

            return [
                {
                    "locality": r[0],
                    "score": round(float(r[1]),1)
                }
                for r in rows
            ]
