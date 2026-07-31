from __future__ import annotations

from collections.abc import Mapping


SUPPORTED_AMENITY_TYPES: frozenset[str] = frozenset(
    {
        "metro_station",
        "bus_stop",
        "hospital",
        "school",
        "restaurant",
        "park",
        "supermarket",
        "gym",
    }
)


def map_osm_category(tags: Mapping[str, str]) -> str | None:
    """Map OSM tags into the frozen NIVAAS amenity taxonomy."""

    amenity = tags.get("amenity")
    shop = tags.get("shop")
    leisure = tags.get("leisure")
    railway = tags.get("railway")
    public_transport = tags.get("public_transport")
    station = tags.get("station")

    # Metro / rapid-transit stations
    if railway == "station" and station in {"subway", "light_rail"}:
        return "metro_station"

    if railway in {"subway_entrance", "halt"} and station == "subway":
        return "metro_station"

    if public_transport == "station" and station == "subway":
        return "metro_station"

    # Bus stops/platforms
    if tags.get("highway") == "bus_stop":
        return "bus_stop"

    if public_transport in {"platform", "stop_position"} and (
        tags.get("bus") == "yes"
        or tags.get("highway") == "bus_stop"
    ):
        return "bus_stop"

    if amenity == "bus_station":
        return "bus_stop"

    # Healthcare
    if amenity in {"hospital", "clinic"}:
        return "hospital"

    # Education
    if amenity == "school":
        return "school"

    # Food
    if amenity in {"restaurant", "fast_food", "food_court"}:
        return "restaurant"

    # Parks
    if leisure in {"park", "garden"}:
        return "park"

    # Grocery
    if shop in {"supermarket", "grocery"}:
        return "supermarket"

    # Fitness
    if leisure in {"fitness_centre", "fitness_station"}:
        return "gym"

    if amenity == "gym":
        return "gym"

    return None
