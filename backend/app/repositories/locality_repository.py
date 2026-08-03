from __future__ import annotations

from typing import Any
from uuid import UUID

import psycopg
from psycopg.rows import dict_row


class LocalityRepository:

    def __init__(self, conn: psycopg.Connection):

        self._conn = conn

    def list_localities(
        self,
        limit: int,
        offset: int,
    ) -> list[dict[str, Any]]:

        query = """
        SELECT
            locality_id,
            name
        FROM core.locality
        ORDER BY name
        LIMIT %s
        OFFSET %s;
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (limit, offset))

            return cur.fetchall()

    def count_localities(self) -> int:

        query = """
        SELECT COUNT(*)
        FROM core.locality;
        """

        with self._conn.cursor() as cur:

            cur.execute(query)

            return cur.fetchone()[0]

    def get_locality(
        self,
        locality_id: UUID,
    ) -> dict[str, Any] | None:

        query = """
        SELECT
            locality_id,
            name
        FROM core.locality
        WHERE locality_id=%s;
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query, (locality_id,))

            return cur.fetchone()
