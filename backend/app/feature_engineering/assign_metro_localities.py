from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def assign_metro_localities():

    init_pool()

    try:

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT COUNT(*)
                    FROM core.amenity
                    WHERE amenity_type = 'metro';
                """)

                print("Metro stations:", cur.fetchone()[0])

                cur.execute("""
                    UPDATE core.amenity a
                    SET locality_id = l.locality_id
                    FROM core.locality l
                    WHERE a.amenity_type = 'metro'
                    AND a.locality_id IS NULL
                    AND ST_Contains(
                        l.boundary,
                        a.geometry
                    );
                """)

                print("Rows updated:", cur.rowcount)

            conn.commit()

    finally:
        close_pool()


if __name__ == "__main__":
    assign_metro_localities()
