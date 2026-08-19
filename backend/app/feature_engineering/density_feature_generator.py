from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def generate_density_score():

    init_pool()

    try:

        with get_connection() as conn:
            with conn.cursor() as cur:

                print("Deleting old density_score...")

                cur.execute("""
                    DELETE FROM feature_store.locality_feature
                    WHERE feature_name = 'density_score';
                """)

                print("Generating density_score...")

                cur.execute("""
                    INSERT INTO feature_store.locality_feature
                    (
                        locality_id,
                        feature_name,
                        feature_value
                    )
                    SELECT
                        locality_id,
                        'density_score',

                        ROUND(
                            (
                                (
                                    feature_value
                                    - MIN(feature_value) OVER ()
                                )
                                /
                                NULLIF(
                                    MAX(feature_value) OVER ()
                                    - MIN(feature_value) OVER (),
                                    0
                                )
                                * 100
                            )::numeric,
                            2
                        )::double precision

                    FROM feature_store.locality_feature
                    WHERE feature_name = 'property_count';
                """)

            conn.commit()

    finally:
        close_pool()

    print("done")


if __name__ == "__main__":
    generate_density_score()
