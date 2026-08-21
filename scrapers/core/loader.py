from __future__ import annotations

import psycopg

from backend.app.config import settings


class DatabaseLoader:

    def __init__(self):
        self.conn = psycopg.connect(settings.DATABASE_URL)

    def insert_amenity(
        self,
        osm_type: str,
        osm_id: int,
        amenity_type: str,
        name: str | None,
        lat: float,
        lon: float,
    ):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO core.amenity(

                    locality_id,
                    osm_type,
                    osm_id,
                    amenity_type,
                    name,
                    latitude,
                    longitude,
                    geometry

                )

                VALUES(

                    NULL,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,

                    ST_SetSRID(
                        ST_Point(%s,%s),
                        4326
                    )

                )

                ON CONFLICT(osm_type,osm_id)
                DO NOTHING;
                """,
                (
                    osm_type,
                    osm_id,
                    amenity_type,
                    name,
                    lat,
                    lon,
                    lon,
                    lat,
                ),
            )

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
