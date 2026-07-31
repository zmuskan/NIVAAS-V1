from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


OsmElementType = Literal["node", "way", "relation"]

SUPPORTED_OSM_TYPES: frozenset[str] = frozenset(
    {"node", "way", "relation"}
)


@dataclass(frozen=True, slots=True)
class AmenityRecord:
    osm_type: OsmElementType
    osm_id: int
    name: str
    amenity_type: str
    latitude: float
    longitude: float
    address: str | None
    tags: dict[str, Any]
