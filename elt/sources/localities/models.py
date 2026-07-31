from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


BoundaryQuality = Literal[
    "verified",
    "osm_boundary",
    "approximate",
]


@dataclass(frozen=True, slots=True)
class LocalityBoundary:
    name: str
    city: str
    state: str

    latitude: float
    longitude: float

    geometry: dict[str, Any]

    source: str
    source_type: str
    source_id: int

    boundary_quality: BoundaryQuality
