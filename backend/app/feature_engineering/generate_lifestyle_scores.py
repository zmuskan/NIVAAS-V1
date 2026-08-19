from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_lifestyle_scores():

    init_pool()

    try:

        with get_connection() as conn:
            with conn.cursor() as cur:

                print("Removing old lifestyle scores...")

                cur.execute("""
                DELETE
                FROM feature_store.locality_feature
                WHERE feature_name IN (
                    'student_score',
                    'family_score',
                    'professional_score'
                );
                """)

                print("student_score")

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    r.locality_id,
                    'student_score',
                    (
                        COALESCE(r.feature_value,0) * 0.70
                        +
                        COALESCE(i.feature_value,0) * 0.30
                    )
                FROM feature_store.locality_feature r

                LEFT JOIN feature_store.locality_feature i
                    ON r.locality_id = i.locality_id
                    AND i.feature_name='inventory_score'

                WHERE r.feature_name='rent_score';
                """)

                print("family_score")

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    locality_id,
                    'family_score',
                    feature_value
                FROM feature_store.locality_feature
                WHERE feature_name='inventory_score';
                """)

                print("professional_score")

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    locality_id,
                    'professional_score',
                    feature_value
                FROM feature_store.locality_feature
                WHERE feature_name='overall_score';
                """)

            conn.commit()

    finally:
        close_pool()

    print("Done")


if __name__ == "__main__":
    generate_lifestyle_scores()
