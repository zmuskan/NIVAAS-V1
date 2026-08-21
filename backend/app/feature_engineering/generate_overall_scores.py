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
                    d.locality_id,
                    'overall_score',

                    (
                        COALESCE(d.feature_value, 0) * 0.40
                        +
                        COALESCE(i.feature_value, 0) * 0.40
                        +
                        COALESCE(ds.feature_value, 0) * 0.20
                    )

                FROM feature_store.locality_feature d

                LEFT JOIN feature_store.locality_feature i
                    ON d.locality_id = i.locality_id
                    AND i.feature_name = 'inventory_score'

                LEFT JOIN feature_store.locality_feature ds
                    ON d.locality_id = ds.locality_id
                    AND ds.feature_name = 'density_score'

                WHERE d.feature_name = 'family_score';
                """)

            conn.commit()

    finally:
        close_pool()

    print("Done")


if __name__ == "__main__":
    generate_overall_scores()
