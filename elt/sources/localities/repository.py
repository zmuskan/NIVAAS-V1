from __future__ import annotations

import json

from psycopg import Connection

from elt.sources.localities.models import LocalityBoundary


class LocalityRepository:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def upsert(self, boundary: LocalityBoundary) -> str:
        geometry_json = json.dumps(boundary.geometry)

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO core.locality (
                    name,
                    city,
                    state,
                    latitude,
                    longitude,
                    geometry,
                    boundary_source,
                    boundary_source_type,
                    boundary_source_id,
                    boundary_quality
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    ST_Multi(
                        ST_SetSRID(
                            ST_GeomFromGeoJSON(%s),
                            4326
                        )
                    ),
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON CONFLICT (name, city, state)
                DO UPDATE SET
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    geometry = EXCLUDED.geometry,
                    boundary_source = EXCLUDED.boundary_source,
                    boundary_source_type = EXCLUDED.boundary_source_type,
                    boundary_source_id = EXCLUDED.boundary_source_id,
                    boundary_quality = EXCLUDED.boundary_quality,
                    updated_at = NOW()
                RETURNING locality_id
                """,
                (
                    boundary.name,
                    boundary.city,
                    boundary.state,
                    boundary.latitude,
                    boundary.longitude,
                    geometry_json,
                    boundary.source,
                    boundary.source_type,
                    boundary.source_id,
                    boundary.boundary_quality,
                ),
            )

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError(
                    f"Failed to persist locality {boundary.name}"
                )

            return str(row[0])

    def delete_implausible_boundaries(
        self,
        minimum_areas: dict[str, float],
    ) -> list[str]:
        """
        Remove locality polygons that are too small to plausibly represent
        the curated NIVAAS target locality.

        Area validation is performed by PostGIS using geography so the
        measurement is expressed in square metres.
        """
        rejected: list[str] = []

        with self.connection.cursor() as cursor:
            for name, minimum_km2 in minimum_areas.items():
                cursor.execute(
                    """
                    DELETE FROM core.locality
                    WHERE name = %s
                      AND geometry IS NOT NULL
                      AND (
                          ST_Area(geometry::geography)
                          / 1000000.0
                      ) < %s
                    RETURNING name
                    """,
                    (
                        name,
                        minimum_km2,
                    ),
                )

                row = cursor.fetchone()

                if row is not None:
                    rejected.append(str(row[0]))

        return rejected

    def assign_amenities(self) -> int:
        """
        Assign amenities to locality polygons using PostGIS.

        ST_Covers is used instead of ST_Contains so amenities exactly on
        polygon boundaries are also eligible for assignment.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE core.amenity AS amenity
                SET locality_id = locality.locality_id
                FROM core.locality AS locality
                WHERE locality.geometry IS NOT NULL
                  AND ST_Covers(
                      locality.geometry,
                      amenity.geometry
                  )
                  AND amenity.locality_id
                      IS DISTINCT FROM locality.locality_id
                """
            )

            return cursor.rowcount
