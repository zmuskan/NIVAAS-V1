from __future__ import annotations

from typing import Any
from uuid import UUID

import psycopg
from psycopg.rows import dict_row


class AnalyticsRepository:

    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    BASE_QUERY = """
        SELECT
            m.locality_id,
            l.name,
            m.listing_count,
            m.avg_rent,
            m.median_rent,
            m.min_rent,
            m.max_rent,
            m.avg_rent_per_sqft,
            m.avg_area_sqft,
            m.avg_bhk,
            m.avg_deposit,
            m.median_deposit,
            m.apartment_pct,
            m.independent_house_pct,
            m.independent_floor_pct,
            m.studio_pct,
            m.villa_pct,
            m.generated_at
        FROM analytics.locality_metrics m
        JOIN core.locality l
        ON l.locality_id = m.locality_id
    """

    def list_all(self) -> list[dict[str, Any]]:

        query = self.BASE_QUERY + " ORDER BY l.name"

        with self._conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_by_locality(
        self,
        locality_id: UUID,
    ) -> dict[str, Any] | None:

        query = self.BASE_QUERY + """
        WHERE m.locality_id=%s
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (locality_id,))

            return cur.fetchone()

    def top_rent(self, limit: int):

        query = (
            self.BASE_QUERY
            + " ORDER BY avg_rent DESC NULLS LAST LIMIT %s"
        )

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (limit,))

            return cur.fetchall()

    def top_listing_count(self, limit: int):

        query = (
            self.BASE_QUERY
            + " ORDER BY listing_count DESC LIMIT %s"
        )

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (limit,))

            return cur.fetchall()
