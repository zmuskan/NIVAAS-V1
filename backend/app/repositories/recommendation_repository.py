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

            COUNT(*) AS listing_count

        FROM core.property p

        JOIN core.locality l
            ON l.locality_id = p.locality_id

        JOIN core.listing li
            ON li.property_id = p.property_id

        GROUP BY l.name
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

            return cur.fetchall()
