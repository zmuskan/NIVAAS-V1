from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row


class RecommendationRepository:

    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def fetch_candidates(
        self,
        min_budget: float,
        max_budget: float,
    ) -> list[dict[str, Any]]:

        query = """

        SELECT
            l.name AS locality,

            ROUND(MIN(li.rent_amount)) AS min_rent,

            ROUND(AVG(li.rent_amount)) AS avg_rent,

            ROUND(MAX(li.rent_amount)) AS max_rent,

            COUNT(DISTINCT li.listing_id) AS listing_count,

            MAX(
                CASE
                    WHEN f.feature_name = 'final_score'
                    THEN f.feature_value
                END
            ) AS final_score,

            MAX(
                CASE
                    WHEN f.feature_name = 'student_score'
                    THEN f.feature_value
                END
            ) AS student_score,

            MAX(
                CASE
                    WHEN f.feature_name = 'family_score'
                    THEN f.feature_value
                END
            ) AS family_score,

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
                    WHEN f.feature_name = 'rent_score'
                    THEN f.feature_value
                END
            ) AS rent_score

        FROM core.property p

        JOIN core.locality l
            ON l.locality_id = p.locality_id

        JOIN core.listing li
            ON li.property_id = p.property_id

        LEFT JOIN feature_store.locality_feature f
            ON l.locality_id = f.locality_id

        GROUP BY l.locality_id, l.name

        HAVING AVG(li.rent_amount) BETWEEN %s AND %s
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    min_budget,
                    max_budget,
                ),
            )

            rows = cur.fetchall()

            print("================================")
            print("FIRST DB ROW")
            print(rows[0] if rows else "NO ROWS")
            print("================================")

            return rows
