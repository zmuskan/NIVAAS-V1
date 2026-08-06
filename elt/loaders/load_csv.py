from pathlib import Path
import argparse

import pandas as pd
import psycopg

from backend.app.config import settings


def load(csv_file: str, amenity_type: str):

    df = pd.read_csv(csv_file)

    conn = psycopg.connect(settings.DATABASE_URL)

    with conn.cursor() as cur:

        for _, row in df.iterrows():

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

                DO UPDATE SET

                    amenity_type=EXCLUDED.amenity_type,
                    name=EXCLUDED.name,
                    latitude=EXCLUDED.latitude,
                    longitude=EXCLUDED.longitude,
                    geometry=EXCLUDED.geometry;
                """,

                (
                    row["osm_type"],
                    int(row["osm_id"]),
                    amenity_type,
                    row["name"],
                    float(row["latitude"]),
                    float(row["longitude"]),
                    float(row["longitude"]),
                    float(row["latitude"]),
                ),
            )

    conn.commit()
    conn.close()

    print(f"Imported {len(df)} {amenity_type} records")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("csv")

    parser.add_argument("type")

    args = parser.parse_args()

    load(args.csv, args.type)
