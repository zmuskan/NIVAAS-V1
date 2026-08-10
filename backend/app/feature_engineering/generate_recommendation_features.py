from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_recommendation_features():

    init_pool()

    try:

        with get_connection() as conn:
            with conn.cursor() as cur:

                print("rent_score")

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    locality_id,
                    'rent_score',
                    ROUND(
                        (
                            100 *
                            (
                                1 -
                                (
                                    feature_value /
                                    MAX(feature_value) OVER ()
                                )
                            )
                        )::numeric,
                        2
                    )::double precision
                FROM feature_store.locality_feature
                WHERE feature_name='avg_rent';
                """)

                print("metro_score")

                cur.execute("""
                INSERT INTO feature_store.locality_feature
                (
                    locality_id,
                    feature_name,
                    feature_value
                )
                SELECT
                    locality_id,
                    'metro_score',
                    LEAST(
                        feature_value * 25,
                        100
                    )
                FROM feature_store.locality_feature
                WHERE feature_name='metro_count';
                """)

            conn.commit()

    finally:
        close_pool()

    print("done")


if __name__ == "__main__":
    generate_recommendation_features()
