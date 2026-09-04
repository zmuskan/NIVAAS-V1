from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_final_scores():

    init_pool()

    try:

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                DELETE
                FROM feature_store.locality_feature
                WHERE feature_name = 'final_score';
                """)

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )

                SELECT

                    locality_id,

                    'final_score',

                    ROUND(
                        (
                            COALESCE(MAX(
                                CASE
                                    WHEN feature_name='rent_score'
                                    THEN feature_value
                                END
                            ),0) * 0.30

                            +

                            COALESCE(MAX(
                                CASE
                                    WHEN feature_name='inventory_score'
                                    THEN feature_value
                                END
                            ),0) * 0.20

                            +

                            COALESCE(MAX(
                                CASE
                                    WHEN feature_name='density_score'
                                    THEN feature_value
                                END
                            ),0) * 0.20

                            +

                            COALESCE(MAX(
                                CASE
                                    WHEN feature_name='student_score'
                                    THEN feature_value
                                END
                            ),0) * 0.15

                            +

                            COALESCE(MAX(
                                CASE
                                    WHEN feature_name='family_score'
                                    THEN feature_value
                                END
                            ),0) * 0.15

                        )::numeric,
                        2
                    )

                FROM feature_store.locality_feature

                GROUP BY locality_id;
                """)

            conn.commit()

    finally:
        close_pool()

    print("final_score generated")


if __name__ == "__main__":
    generate_final_scores()
