from __future__ import annotations

from dataclasses import dataclass

from psycopg import Connection

from elt.sources.osm.models import AmenityRecord


@dataclass(frozen=True, slots=True)
class UpsertCounts:
    processed: int


class AmenityRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def upsert_many(
        self,
        amenities: list[AmenityRecord],
    ) -> UpsertCounts:
        if not amenities:
            return UpsertCounts(processed=0)

        sql = """
            INSERT INTO core.amenity (
                name,
                amenity_type,
                address,
                latitude,
                longitude,
                geometry,
                osm_type,
                osm_id,
                updated_at
            )
            VALUES (
                %(name)s,
                %(amenity_type)s,
                %(address)s,
                %(latitude)s,
                %(longitude)s,
                ST_SetSRID(
                    ST_MakePoint(
                        %(longitude)s,
                        %(latitude)s
                    ),
                    4326
                ),
                %(osm_type)s,
                %(osm_id)s,
                NOW()
            )
            ON CONFLICT (osm_type, osm_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                amenity_type = EXCLUDED.amenity_type,
                address = EXCLUDED.address,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                geometry = EXCLUDED.geometry,
                updated_at = NOW()
        """

        parameters = [
            {
                "name": amenity.name,
                "amenity_type": amenity.amenity_type,
                "address": amenity.address,
                "latitude": amenity.latitude,
                "longitude": amenity.longitude,
                "osm_type": amenity.osm_type,
                "osm_id": amenity.osm_id,
            }
            for amenity in amenities
        ]

        with self._connection.cursor() as cursor:
            cursor.executemany(sql, parameters)

        return UpsertCounts(processed=len(amenities))
