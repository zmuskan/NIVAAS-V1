from fastapi import APIRouter, HTTPException

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
                    ) AS overall_score,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'inventory_score'
                            THEN f.feature_value
                        END
                    ) AS inventory_score,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'density_score'
                            THEN f.feature_value
                        END
                    ) AS density_score

                FROM core.locality l

                LEFT JOIN feature_store.locality_feature f
                    ON l.locality_id = f.locality_id

                GROUP BY l.locality_id, l.name

                ORDER BY l.name
                """
            )

            rows = cur.fetchall()

            items = []

            for row in rows:
                items.append(
                    {
                        "locality": row[0],
                        "avg_rent": (
                            round(float(row[1]), 0)
                            if row[1] is not None
                            else None
                        ),
                        "listing_count": (
                            float(row[2])
                            if row[2] is not None
                            else None
                        ),
                        "overall_score": (
                            round(float(row[3]), 1)
                            if row[3] is not None
                            else None
                        ),
                        "inventory_score": (
                            round(float(row[4]), 1)
                            if row[4] is not None
                            else None
                        ),
                        "density_score": (
                            round(float(row[5]), 1)
                            if row[5] is not None
                            else None
                        ),
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
                            WHEN f.feature_name = 'min_rent'
                            THEN f.feature_value
                        END
                    ) AS min_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'avg_rent'
                            THEN f.feature_value
                        END
                    ) AS avg_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'max_rent'
                            THEN f.feature_value
                        END
                    ) AS max_rent,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'listing_count'
                            THEN f.feature_value
                        END
                    ) AS listing_count,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'property_count'
                            THEN f.feature_value
                        END
                    ) AS property_count,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'overall_score'
                            THEN f.feature_value
                        END
                    ) AS overall_score,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'inventory_score'
                            THEN f.feature_value
                        END
                    ) AS inventory_score,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'density_score'
                            THEN f.feature_value
                        END
                    ) AS density_score,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'centroid_lat'
                            THEN f.feature_value
                        END
                    ) AS centroid_lat,

                    MAX(
                        CASE
                            WHEN f.feature_name = 'centroid_lon'
                            THEN f.feature_value
                        END
                    ) AS centroid_lon

                FROM core.locality l

                LEFT JOIN feature_store.locality_feature f
                    ON l.locality_id = f.locality_id

                WHERE LOWER(l.name) = LOWER(%s)

                GROUP BY l.locality_id, l.name
                """,
                (locality_name,),
            )

            row = cur.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Locality not found",
                )

            return {
                "name": row[0],

                "min_rent": (
                    round(float(row[1]), 0)
                    if row[1] is not None
                    else None
                ),

                "avg_rent": (
                    round(float(row[2]), 0)
                    if row[2] is not None
                    else None
                ),

                "max_rent": (
                    round(float(row[3]), 0)
                    if row[3] is not None
                    else None
                ),

                "listing_count": (
                    float(row[4])
                    if row[4] is not None
                    else None
                ),

                "property_count": (
                    float(row[5])
                    if row[5] is not None
                    else None
                ),

                "overall_score": (
                    round(float(row[6]), 1)
                    if row[6] is not None
                    else None
                ),

                "inventory_score": (
                    round(float(row[7]), 1)
                    if row[7] is not None
                    else None
                ),

                "density_score": (
                    round(float(row[8]), 1)
                    if row[8] is not None
                    else None
                ),

                "centroid_lat": (
                    float(row[9])
                    if row[9] is not None
                    else None
                ),

                "centroid_lon": (
                    float(row[10])
                    if row[10] is not None
                    else None
                ),
            }
