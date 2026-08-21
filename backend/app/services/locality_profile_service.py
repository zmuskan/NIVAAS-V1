from backend.app.repositories.locality_profile_repository import (
    get_locality_profile,
)


def fetch_locality_profile(locality_name: str):

    row = get_locality_profile(locality_name)

    print("LOCALITY =", locality_name)
    print("ROW =", row)

    if not row:
        return None

    return {

        "name": row[0],

        "min_rent": round(float(row[1]), 0) if row[1] else None,

        "avg_rent": round(float(row[2]), 0) if row[2] else None,

        "max_rent": round(float(row[3]), 0) if row[3] else None,

        "listing_count": int(row[4]) if row[4] else 0,

        "avg_bhk": round(float(row[5]), 1) if row[5] else None,

        "avg_area_sqft": round(float(row[6]), 0) if row[6] else None,
    }
