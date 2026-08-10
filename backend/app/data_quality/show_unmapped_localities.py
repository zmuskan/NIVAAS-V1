from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def show_unmapped():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    name
                FROM core.locality
                WHERE locality_id NOT IN
                (
                    SELECT locality_id
                    FROM analytics.locality_mapping
                )
                ORDER BY name
                """
            )

            rows = cur.fetchall()

    print(f"unmapped: {len(rows)}")

    for row in rows[:200]:
        print(row[0])


if __name__ == "__main__":

    init_pool()

    try:
        show_unmapped()
    finally:
        close_pool()
