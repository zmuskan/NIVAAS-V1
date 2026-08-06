import json
from pathlib import Path

import psycopg

from backend.app.config import settings

FILE = Path("data/raw/bbmp_wards.geojson")


def main():

    with open(FILE, encoding="utf-8") as f:
        geo = json.load(f)

    conn = psycopg.connect(settings.DATABASE_URL)

    with conn.cursor() as cur:

        imported = 0

        for feature in geo["features"]:

            props = feature["properties"]
            geometry = feature["geometry"]

            if geometry["type"] not in ("Polygon", "MultiPolygon"):
                continue

            name = (
                props.get("WARD_NAME")
                or props.get("Ward_Name")
                or props.get("NAME")
                or props.get("name")
                or f"Ward {imported+1}"
            )

            geom_json = json.dumps(geometry)

            cur.execute(
                """
                INSERT INTO core.locality
                (
                    name,
                    city,
                    state,
                    country,
                    boundary,
                    centroid,
                    latitude,
                    longitude
                )

                VALUES
                (
                    %s,
                    'Bengaluru',
                    'Karnataka',
                    'India',

                    ST_SetSRID(
                        ST_GeomFromGeoJSON(%s),
                        4326
                    ),

                    ST_Centroid(
                        ST_SetSRID(
                            ST_GeomFromGeoJSON(%s),
                            4326
                        )
                    ),

                    ST_Y(
                        ST_Centroid(
                            ST_SetSRID(
                                ST_GeomFromGeoJSON(%s),
                                4326
                            )
                        )
                    ),

                    ST_X(
                        ST_Centroid(
                            ST_SetSRID(
                                ST_GeomFromGeoJSON(%s),
                                4326
                            )
                        )
                    )

                )

                ON CONFLICT(name,city)

                DO NOTHING;
                """,
                (
                    name,
                    geom_json,
                    geom_json,
                    geom_json,
                    geom_json,
                ),
            )

            imported += 1

    conn.commit()
    conn.close()

    print(f"Imported {imported} wards.")


if __name__ == "__main__":
    main()
