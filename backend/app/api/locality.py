from fastapi import APIRouter

from backend.app.database import get_connection

router = APIRouter(
    prefix="/localities",
    tags=["localities"],
)

@router.get("")
def get_all_localities():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT

                    l.name,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'avg_rent'
                            THEN f.feature_value
                        END
                    ) AS avg_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'listing_count'
                            THEN f.feature_value
                        END
                    ) AS listing_count,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'overall_score'
                            THEN f.feature_value
                        END
                    ) AS overall_score

                FROM core.locality l

                JOIN feature_store.locality_feature f
                    ON l.locality_id = f.locality_id

                GROUP BY l.name

                ORDER BY l.name
                """
            )

            rows = cur.fetchall()

            items = []

            for row in rows:
                items.append(
                    {
                        "locality": row[0],
                        "avg_rent": round(float(row[1]), 0) if row[1] else None,
                        "listing_count": row[2],
                        "overall_score": round(float(row[3]), 1) if row[3] else None,
                    }
                )

            return {
                "items": items,
                "total": len(items),
            }

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
                            WHEN f.feature_name='overall_score'
                            THEN f.feature_value
                        END
                    ) AS overall_score,

                    MAX(
                        CASE
                            WHEN f.feature_name='inventory_score'
                            THEN f.feature_value
                        END
                    ) AS inventory_score,

                    MAX(
                        CASE
                            WHEN f.feature_name='density_score'
                            THEN f.feature_value
                        END
                    ) AS density_score

                    MAX(
                        CASE
                            WHEN f.feature_name='centroid_lat'
                            THEN f.feature_value
                        END
                    ) AS centroid_lat,

                    MAX(
                        CASE
                            WHEN f.feature_name='centroid_lon'
                            THEN f.feature_value
                        END
                    ) AS centroid_lon

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

                "min_rent": round(float(row[1]), 0) if row[1] else None,

                "avg_rent": round(float(row[2]), 0) if row[2] else None,

                "max_rent": round(float(row[3]), 0) if row[3] else None,

                "listing_count": row[4],

                "property_count": row[5],

                "overall_score": round(float(row[6]), 1) if row[6] else None,

                "inventory_score": round(float(row[7]), 1) if row[7] else None,

                "density_score": round(float(row[8]), 1) if row[8] else None,

                "centroid_lat": float(row[9]) if row[9] else None,

                "centroid_lon": float(row[10]) if row[10] else None,
            }
