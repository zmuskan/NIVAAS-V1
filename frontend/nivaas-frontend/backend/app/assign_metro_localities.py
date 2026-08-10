from backend.app.database import get_connection


def assign_metro_localities():

    with get_connection() as conn:
        with conn.cursor() as cur:

            print("Assigning nearest locality to metro stations...")

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

        conn.commit()

    print("Done")


if __name__ == "__main__":
    assign_metro_localities()
