from __future__ import annotations

from typing import Any

from elt.sources.localities.models import LocalityBoundary
from elt.sources.localities.registry import TargetLocality


SUPPORTED_OSM_TYPES = {"relation", "way"}

LOCALITY_CATEGORIES = {
    "boundary",
    "place",
}


def normalize_candidate(
    target: TargetLocality,
    candidate: dict[str, Any],
) -> LocalityBoundary | None:
    osm_type = candidate.get("osm_type")
    osm_id = candidate.get("osm_id")
    geojson = candidate.get("geojson")

    if osm_type not in SUPPORTED_OSM_TYPES:
        return None

    if not isinstance(osm_id, int):
        return None

    if not isinstance(geojson, dict):
        return None

    if geojson.get("type") not in {"Polygon", "MultiPolygon"}:
        return None

    try:
        latitude = float(candidate["lat"])
        longitude = float(candidate["lon"])
    except (KeyError, TypeError, ValueError):
        return None

    if not 12.70 <= latitude <= 13.25:
        return None

    if not 77.30 <= longitude <= 77.90:
        return None

    category = candidate.get("category")

    if category is not None and category not in LOCALITY_CATEGORIES:
        return None

    return LocalityBoundary(
        name=target.name,
        city=target.city,
        state=target.state,
        latitude=latitude,
        longitude=longitude,
        geometry=geojson,
        source="OpenStreetMap",
        source_type=osm_type,
        source_id=osm_id,
        boundary_quality="osm_boundary",
    )


def select_boundary(
    target: TargetLocality,
    candidates: list[dict[str, Any]],
) -> LocalityBoundary | None:
    for candidate in candidates:
        boundary = normalize_candidate(target, candidate)

        if boundary is not None:
            return boundary

    return None
