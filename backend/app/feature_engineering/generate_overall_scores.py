from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_overall_scores():

    init_pool()

    try:

        with get_connection() as conn:
            with conn.cursor() as cur:

                print("Removing old overall_score...")

                cur.execute("""
                DELETE
                FROM feature_store.locality_feature
                WHERE feature_name = 'overall_score';
                """)

                print("Generating overall_score...")

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    r.locality_id,
                    'overall_score',
                    (
                        COALESCE(r.feature_value, 0) * 0.70
                        +
                        COALESCE(m.feature_value, 0) * 0.30
                    )
                FROM feature_store.locality_feature r
                LEFT JOIN feature_store.locality_feature m
                    ON r.locality_id = m.locality_id
                    AND m.feature_name = 'metro_score'
                WHERE r.feature_name = 'rent_score';
                """)

            conn.commit()

    finally:
        close_pool()

    print("Done")


if __name__ == "__main__":
    generate_overall_scores()
