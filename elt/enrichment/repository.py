from __future__ import annotations

from psycopg.rows import dict_row

from elt.common.config import settings
from elt.common.database import get_connection


class EnrichmentRepository:

    def __init__(self):

        self._ctx = get_connection(settings)
        self._conn = self._ctx.__enter__()

    # ------------------------------------------------------------
    # Fetch localities
    # ------------------------------------------------------------

    def fetch_localities(self):

        query = """
        SELECT
            locality_id,
            name,
            ST_Y(centroid) AS latitude,
            ST_X(centroid) AS longitude
        FROM core.locality
        ORDER BY name;
        """

        with self._conn.cursor(row_factory=dict_row) as cur:

            cur.execute(query)

            return cur.fetchall()

    # ------------------------------------------------------------
    # Save POIs
    # ------------------------------------------------------------

    def save_pois(self, pois):

        if not pois:
            return

        query = """
        INSERT INTO geo.poi
        (
            name,
            category,
            latitude,
            longitude,
            locality,
            source
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT DO NOTHING;
        """

        with self._conn.cursor() as cur:

            for poi in pois:

                cur.execute(
                    query,
                    (
                        poi["name"],
                        poi["category"],
                        poi["latitude"],
                        poi["longitude"],
                        poi["locality"],
                        poi["source"],
                    )
                )

        self._conn.commit()

    # ------------------------------------------------------------
    # Count POIs
    # ------------------------------------------------------------

    def count_pois(self):

        query = """
        SELECT COUNT(*)
        FROM geo.poi;
        """

        with self._conn.cursor() as cur:

            cur.execute(query)

            return cur.fetchone()[0]

    # ------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------

    def close(self):

        self._ctx.__exit__(None, None, None)
