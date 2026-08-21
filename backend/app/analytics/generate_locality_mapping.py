from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)




RULES = [

        ("hsr", "HSR Layout"),

        ("koramangala", "Koramangala"),

        ("jp nagar", "JP Nagar"),

        ("jayanagar", "Jayanagar"),

        ("btm", "BTM Layout"),

        ("electronic city", "Electronic City"),

        ("electronics city", "Electronic City"),

        ("whitefield", "Whitefield"),

        ("bellandur", "Bellandur"),

        ("marathahalli", "Marathahalli"),

        ("indira nagar", "Indiranagar"),

        ("indiranagar", "Indiranagar"),

        ("mahadevapura", "Mahadevapura"),

        ("kr puram", "KR Puram"),

        ("krishnarajapura", "KR Puram"),

        ("hebbal", "Hebbal"),

        ("yelahanka", "Yelahanka"),

        ("sarjapur", "Sarjapur"),

        ("kengeri", "Kengeri"),

        ("rajajinagar", "Rajajinagar"),

        ("banashankari", "Banashankari"),

        ("basavanagudi", "Basavanagudi"),

        ("basaveshwaranagar", "Basaveshwaranagar"),

        ("rr nagar", "RR Nagar"),

        ("rajarajeshwari nagar", "RR Nagar"),

        ("bommanahalli", "Bommanahalli"),

        ("bommasandra", "Bommasandra"),

        ("brookefield", "Brookefield"),

        ("hoodi", "Hoodi"),

        ("kadugodi", "Kadugodi"),

        ("attibele", "Attibele"),

        ("begur", "Begur"),

        ("bannerghatta", "Bannerghatta"),

        ("arekere", "Arekere"),

        ("arakere", "Arekere"),

        ("aecs", "AECS Layout"),

        ("cv raman", "CV Raman Nagar"),

    ]

def generate_mapping():

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                DELETE FROM analytics.locality_mapping;
            """)

            cur.execute("""
                SELECT locality_id, name
                FROM core.locality;
            """)

            rows = cur.fetchall()

            inserted = 0

            for locality_id, name in rows:

                canonical = None

                lower_name = name.lower()

                for keyword, target in RULES:

                    if keyword.lower() in lower_name:
                        canonical = target
                        break

                if canonical:

                    cur.execute(
                        """
                        INSERT INTO analytics.locality_mapping
                        (
                            locality_id,
                            locality_name,
                            canonical_locality
                        )
                        VALUES (%s,%s,%s)
                        """,
                        (
                            locality_id,
                            name,
                            canonical,
                        ),
                    )

                    inserted += 1

            conn.commit()

            print(f"Mapped: {inserted}")
if __name__ == "__main__":

    init_pool()

    try:
        generate_mapping()

    finally:
        close_pool()
