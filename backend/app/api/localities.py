from fastapi import APIRouter
from backend.app.database import get_connection

router = APIRouter(
    prefix="/localities",
    tags=["localities"],
)
print("LOCALITIES FILE LOADED")
@router.get("")
def get_all_localities():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT l.name
                FROM analytics.locality_metrics lm
                JOIN core.locality l
                    ON l.locality_id = lm.locality_id
                ORDER BY l.name
            """)

            rows = cur.fetchall()

            return {
                "items": [row[0] for row in rows]
            }
