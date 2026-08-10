from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_locality_features():

    with get_connection() as conn:
        with conn.cursor() as cur:

            print("Clearing old features...")

            cur.execute("""
                DELETE FROM feature_store.locality_feature;
            """)

            print("avg_rent")

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

            print("min_rent")

            cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    p.locality_id,
                    'min_rent',
                    MIN(l.rent_amount)::DOUBLE PRECISION
                FROM core.property p
                JOIN core.listing l
                    ON p.property_id = l.property_id
                GROUP BY p.locality_id;
            """)

            print("max_rent")

            cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    p.locality_id,
                    'max_rent',
                    MAX(l.rent_amount)::DOUBLE PRECISION
                FROM core.property p
                JOIN core.listing l
                    ON p.property_id = l.property_id
                GROUP BY p.locality_id;
            """)

            print("listing_count")

            cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    p.locality_id,
                    'listing_count',
                    COUNT(*)::DOUBLE PRECISION
                FROM core.property p
                JOIN core.listing l
                    ON p.property_id = l.property_id
                GROUP BY p.locality_id;
            """)

            print("property_count")

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

            print("metro_count skipped")

        conn.commit()

    print("Done")


if __name__ == "__main__":

    init_pool()

    try:
        generate_locality_features()

    finally:
        close_pool()
