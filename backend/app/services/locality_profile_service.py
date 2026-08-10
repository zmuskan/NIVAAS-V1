from backend.app.repositories.locality_profile_repository import (
    get_locality_profile,
)


def fetch_locality_profile(locality_name: str):

    row = get_locality_profile(locality_name)

    if not row:
        return None

    return {
        "name": row[0],
        "min_rent": row[1],
        "avg_rent": row[2],
        "max_rent": row[3],
        "listing_count": row[4],
        "property_count": row[5],
        "metro_count": row[6],
    }
