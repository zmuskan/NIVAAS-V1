from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


AreaType = Literal["locality", "corridor"]


@dataclass(frozen=True, slots=True)
class TargetLocality:
    name: str
    city: str = "Bengaluru"
    state: str = "Karnataka"
    area_type: AreaType = "locality"
    min_area_km2: float = 0.25


TARGET_LOCALITIES: tuple[TargetLocality, ...] = (
    TargetLocality("HSR Layout"),
    TargetLocality("Koramangala"),
    TargetLocality("Indiranagar"),
    TargetLocality("Whitefield"),
    TargetLocality("Bellandur"),
    TargetLocality("Marathahalli"),
    TargetLocality("BTM Layout"),
    TargetLocality("JP Nagar"),
    TargetLocality("Jayanagar"),
    TargetLocality("Electronic City"),
    TargetLocality("Brookefield"),
    TargetLocality("Ulsoor"),
    TargetLocality(
        "Sarjapur Road",
        area_type="corridor",
    ),
    TargetLocality(
        "Bannerghatta Road",
        area_type="corridor",
    ),
    TargetLocality("Sadashivanagar"),
)
