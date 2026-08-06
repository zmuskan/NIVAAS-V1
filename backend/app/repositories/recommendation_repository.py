from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row


class RecommendationRepository:

    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def fetch_candidates(
        self,
        budget: float,
    ) -> list[dict[str, Any]]:

        query = """
        SELECT

            p.property_id,
            p.locality_id,
            l.name AS locality_name,

            p.property_type,
            p.bhk,
            p.area_sqft,
            p.furnishing_status,

            li.rent_amount,

            la.listing_count,
            la.avg_rent,
            la.avg_rent_per_sqft,
            la.apartment_pct,
            la.independent_house_pct,
            la.villa_pct

        FROM core.property p

        JOIN core.locality l
            ON l.locality_id=p.locality_id

        JOIN core.listing li
            ON li.property_id=p.property_id

        LEFT JOIN analytics.locality_summary la
            ON la.locality_id=p.locality_id

        WHERE li.rent_amount<=%s
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (budget,))
            return cur.fetchall()
