from fastapi import APIRouter

from backend.app.database import get_connection

router = APIRouter(
    prefix="/localities",
    tags=["localities"],
)


@router.get("/{locality_name}")
def get_locality(locality_name: str):

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT

                    l.name,

                    MAX(
                        CASE
                            WHEN f.feature_name='min_rent'
                            THEN f.feature_value
                        END
                    ) AS min_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name='avg_rent'
                            THEN f.feature_value
                        END
                    ) AS avg_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name='max_rent'
                            THEN f.feature_value
                        END
                    ) AS max_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name='listing_count'
                            THEN f.feature_value
                        END
                    ) AS listing_count,

                    MAX(
                        CASE
                            WHEN f.feature_name='property_count'
                            THEN f.feature_value
                        END
                    ) AS property_count,

                    MAX(
                        CASE
                            WHEN f.feature_name='metro_count'
                            THEN f.feature_value
                        END
                    ) AS metro_count

                FROM core.locality l

                LEFT JOIN feature_store.locality_feature f
                    ON l.locality_id = f.locality_id

                WHERE l.name ILIKE %s

                GROUP BY l.name
                """,
                (locality_name,)
            )

            row = cur.fetchone()

            if row is None:
                return {"error": "Locality not found"}

            return {
                "name": row[0],
                "min_rent": row[1],
                "avg_rent": row[2],
                "max_rent": row[3],
                "listing_count": row[4],
                "property_count": row[5],
                "metro_count": row[6]
            }
