from pathlib import Path

import pandas as pd
import psycopg

from backend.app.config import settings

CSV = Path("data/raw/metro.csv")


def main():

    df = pd.read_csv(CSV)

    print(df.head())
    print(df.columns.tolist())

    conn = psycopg.connect(settings.DATABASE_URL)

    with conn.cursor() as cur:

        for _, row in df.iterrows():

            cur.execute(
                """
                INSERT INTO core.amenity (

                    locality_id,
                    osm_type,
                    osm_id,
                    amenity_type,
                    name,
                    latitude,
                    longitude,
                    geometry

                )

                VALUES (

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

                ON CONFLICT (osm_type, osm_id)
                DO UPDATE SET

                    amenity_type = EXCLUDED.amenity_type,
                    name = EXCLUDED.name,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude,
                    geometry = EXCLUDED.geometry;
                """,
                (
                    str(row["osm_type"]),
                    int(row["osm_id"]),
                    str(row["amenity_type"]),
                    str(row["name"]),
                    float(row["latitude"]),
                    float(row["longitude"]),
                    float(row["longitude"]),
                    float(row["latitude"]),
                ),
            )

    conn.commit()
    conn.close()

    print(f"\nImported {len(df)} amenities successfully.")


if __name__ == "__main__":
    main()
