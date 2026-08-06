from pathlib import Path
import argparse
import json

import psycopg

from backend.app.config import settings


def load(file_path: str, amenity_type: str):

    path = Path(file_path)

    with open(path, encoding="utf-8") as f:
        geo = json.load(f)

    conn = psycopg.connect(settings.DATABASE_URL)

    with conn.cursor() as cur:

        count = 0

        for feature in geo["features"]:

            geometry = feature.get("geometry")

            if not geometry:
                continue

            if geometry["type"] != "Point":
                continue

            props = feature.get("properties", {})

            coords = geometry["coordinates"]

            lon = coords[0]
            lat = coords[1]

            osm_id = props.get("id", count + 1)

            name = (
                props.get("name")
                or props.get("station")
                or props.get("NAME")
                or f"{amenity_type}_{count+1}"
            )

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
                    'geojson',
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

                DO UPDATE SET

                    amenity_type=EXCLUDED.amenity_type,
                    name=EXCLUDED.name,
                    latitude=EXCLUDED.latitude,
                    longitude=EXCLUDED.longitude,
                    geometry=EXCLUDED.geometry;
                """,
                (
                    osm_id,
                    amenity_type,
                    name,
                    lat,
                    lon,
                    lon,
                    lat,
                ),
            )

            count += 1

    conn.commit()

    conn.close()

    print(f"Imported {count} records.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("file")

    parser.add_argument("type")

    args = parser.parse_args()

    load(args.file, args.type)
