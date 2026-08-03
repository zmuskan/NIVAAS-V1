from __future__ import annotations

from typing import Any
from uuid import UUID

import psycopg
from psycopg.rows import dict_row


class PropertyRepository:

    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    BASE_QUERY = """
        SELECT

            p.property_id,
            p.locality_id,
            l.name AS locality_name,

            p.property_type,
            p.bhk,
            p.bathrooms,
            p.area_sqft,
            p.furnishing_status,
            p.latitude,
            p.longitude,

            li.listing_id,
            li.rent_amount,
            li.deposit_amount,
            li.maintenance_amount,
            li.listing_status,
            li.title,
            li.description,
            li.listing_url

        FROM core.property p

        JOIN core.locality l
        ON l.locality_id = p.locality_id

        JOIN core.listing li
        ON li.property_id = p.property_id
    """

    def list_properties(
        self,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:

        query = (
            self.BASE_QUERY
            + """
            ORDER BY li.rent_amount
            LIMIT %s
            OFFSET %s
            """
        )

        with self._conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (limit, offset))
            return cur.fetchall()

    def count_properties(self) -> int:

        query = """
            SELECT COUNT(*)
            FROM core.property
        """

        with self._conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()[0]

    def get_property(
        self,
        property_id: UUID,
    ) -> dict[str, Any] | None:

        query = (
            self.BASE_QUERY
            + """
            WHERE p.property_id=%s
            """
        )

        with self._conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (property_id,))
            return cur.fetchone()

    def get_by_locality(
        self,
        locality_id: UUID,
    ) -> list[dict[str, Any]]:

        query = (
            self.BASE_QUERY
            + """
            WHERE p.locality_id=%s
            ORDER BY li.rent_amount
            """
        )

        with self._conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, (locality_id,))
            return cur.fetchall()

    def search(
        self,
        min_rent: float | None,
        max_rent: float | None,
        bhk: int | None,
    ) -> list[dict[str, Any]]:

        query = self.BASE_QUERY + """
        WHERE
            (%s IS NULL OR li.rent_amount >= %s)
        AND (%s IS NULL OR li.rent_amount <= %s)
        AND (%s IS NULL OR p.bhk = %s)

        ORDER BY li.rent_amount
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                query,
                (
                    min_rent,
                    min_rent,
                    max_rent,
                    max_rent,
                    bhk,
                    bhk,
                ),
            )

            return cur.fetchall()

    def get_recommendations(
        self,
        budget: float,
        bhk: int | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        query = self.BASE_QUERY + """
        WHERE
            li.rent_amount <= %s
            AND (%s IS NULL OR p.bhk = %s)

        ORDER BY
            li.rent_amount ASC,
            p.area_sqft DESC

        LIMIT %s
        """

        with self._conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                query,
                (
                    budget,
                    bhk,
                    bhk,
                    limit,
                ),
            )
            return cur.fetchall()
