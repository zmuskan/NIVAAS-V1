from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)

from backend.app.data_quality.canonical_localities import (
    CANONICAL_LOCALITIES,
)


def load_mapping():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                DELETE FROM analytics.locality_mapping;
                """
            )

            for canonical, aliases in CANONICAL_LOCALITIES.items():

                cur.execute(
                    """
                    INSERT INTO analytics.locality_mapping
                    (
                        locality_id,
                        locality_name,
                        canonical_locality
                    )
                    SELECT
                        locality_id,
                        name,
                        %s
                    FROM core.locality
                    WHERE name = ANY(%s)
                    """,
                    (
                        canonical,
                        aliases,
                    ),
                )

        conn.commit()

    print("mapping loaded")


if __name__ == "__main__":

    init_pool()

    try:
        load_mapping()
    finally:
        close_pool()
