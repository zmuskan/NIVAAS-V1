from __future__ import annotations

from typing import Any

from elt.sources.osm.mapping import map_osm_category
from elt.sources.osm.models import (
    AmenityRecord,
    SUPPORTED_OSM_TYPES,
)


def _extract_coordinates(
    element: dict[str, Any],
) -> tuple[float, float] | None:
    osm_type = element.get("type")

    if osm_type == "node":
        latitude = element.get("lat")
        longitude = element.get("lon")
    else:
        center = element.get("center") or {}
        latitude = center.get("lat")
        longitude = center.get("lon")

    if latitude is None or longitude is None:
        return None

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return None

    if not (-90 <= latitude <= 90):
        return None

    if not (-180 <= longitude <= 180):
        return None

    return latitude, longitude


def _build_address(tags: dict[str, Any]) -> str | None:
    house_number = tags.get("addr:housenumber")
    street = tags.get("addr:street")
    suburb = tags.get("addr:suburb")
    city = tags.get("addr:city")
    postcode = tags.get("addr:postcode")

    components: list[str] = []

    if house_number and street:
        components.append(f"{house_number} {street}")
    else:
        if house_number:
            components.append(str(house_number))
        if street:
            components.append(str(street))

    for value in (suburb, city, postcode):
        if value:
            components.append(str(value))

    if not components:
        return None

    return ", ".join(components)


def normalize_element(
    element: dict[str, Any],
) -> AmenityRecord | None:
    osm_type = element.get("type")

    if osm_type not in SUPPORTED_OSM_TYPES:
        return None

    osm_id = element.get("id")

    if osm_id is None:
        return None

    try:
        osm_id = int(osm_id)
    except (TypeError, ValueError):
        return None

    if osm_id <= 0:
        return None

    raw_tags = element.get("tags")

    if not isinstance(raw_tags, dict):
        return None

    tags = {
        str(key): str(value)
        for key, value in raw_tags.items()
        if value is not None
    }

    amenity_type = map_osm_category(tags)

    if amenity_type is None:
        return None

    coordinates = _extract_coordinates(element)

    if coordinates is None:
        return None

    latitude, longitude = coordinates

    # core.amenity.name is NOT NULL.
    # OSM objects are sometimes unnamed, so use a deterministic fallback.
    name = tags.get("name")

    if not name or not name.strip():
        name = f"Unnamed {amenity_type.replace('_', ' ')}"

    return AmenityRecord(
        osm_type=osm_type,
        osm_id=osm_id,
        name=name.strip()[:255],
        amenity_type=amenity_type,
        latitude=latitude,
        longitude=longitude,
        address=_build_address(tags),
        tags=tags,
    )
