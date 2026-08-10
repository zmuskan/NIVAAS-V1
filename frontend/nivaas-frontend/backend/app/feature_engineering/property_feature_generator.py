from backend.app.database import get_connection


def generate_property_features():

    with get_connection() as conn:
        with conn.cursor() as cur:

            print("Clearing property features...")

            cur.execute("""
                DELETE FROM feature_store.property_feature;
            """)

            print("Generating property features...")

            cur.execute("""
                INSERT INTO feature_store.property_feature
                (
                    property_id,
                    metro_distance_m,
                    rent_per_sqft,
                    amenity_density
                )
                SELECT
                    p.property_id,

                    (
                        SELECT
                            MIN(
                                ST_Distance(
                                    p.geometry::geography,
                                    a.geometry::geography
                                )
                            )
                        FROM core.amenity a
                        WHERE a.amenity_type = 'metro'
                    ) AS metro_distance_m,

                    CASE
                        WHEN p.area_sqft > 0
                        THEN l.rent_amount / p.area_sqft
                        ELSE NULL
                    END AS rent_per_sqft,

                    0 AS amenity_density

                FROM core.property p
                JOIN core.listing l
                    ON p.property_id = l.property_id;
            """)

        conn.commit()

    print("Property features generated")


if __name__ == "__main__":
    generate_property_features()    
