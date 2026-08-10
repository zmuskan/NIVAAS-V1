from backend.app.database import get_connection


def generate_locality_features():

    with get_connection() as conn:
        with conn.cursor() as cur:

            print("Clearing old features...")

            cur.execute("""
                DELETE FROM feature_store.locality_feature;
            """)

            print("Generating avg_rent...")

            cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    p.locality_id,
                    'avg_rent',
                    AVG(l.rent_amount)::DOUBLE PRECISION
                FROM core.property p
                JOIN core.listing l
                    ON p.property_id = l.property_id
                GROUP BY p.locality_id;
            """)

            print("Generating property_count...")

            cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    locality_id,
                    'property_count',
                    COUNT(*)::DOUBLE PRECISION
                FROM core.property
                GROUP BY locality_id;
            """)

            print("Generating metro_score...")

            cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    l.locality_id,
                    'metro_score',
                    COUNT(a.amenity_id)::DOUBLE PRECISION
                FROM core.locality l
                LEFT JOIN core.amenity a
                    ON l.locality_id = a.locality_id
                    AND a.amenity_type = 'metro'
                GROUP BY l.locality_id;
            """)

        conn.commit()

    print("Feature generation complete")


if __name__ == "__main__":
    generate_locality_features()
