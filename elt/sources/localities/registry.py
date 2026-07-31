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
    search_aliases: tuple[str, ...] = ()

    @property
    def search_names(self) -> tuple[str, ...]:
        return (self.name, *self.search_aliases)


TARGET_LOCALITIES: tuple[TargetLocality, ...] = (
    TargetLocality(
        "HSR Layout",
        search_aliases=("HSR",),
    ),
    TargetLocality(
        "Koramangala",
        search_aliases=(
            "Koramangala 1st Block",
            "Koramangala 3rd Block",
        ),
    ),
    TargetLocality("Indiranagar"),
    TargetLocality("Whitefield"),
    TargetLocality("Bellandur"),
    TargetLocality("Marathahalli"),
    TargetLocality(
        "BTM Layout",
        search_aliases=(
            "BTM 1st Stage",
            "BTM 2nd Stage",
            "Byrasandra Tavarekere Madiwala",
        ),
    ),
    TargetLocality(
        "JP Nagar",
        search_aliases=("J P Nagar",),
    ),
    TargetLocality(
        "Jayanagar",
        search_aliases=(
            "Jayanagara",
            "Jayanagar 4th Block",
        ),
    ),
    TargetLocality(
        "Electronic City",
        min_area_km2=0.50,
        search_aliases=(
            "Electronics City",
            "Electronic City Phase 1",
            "Electronic City Phase 2",
        ),
    ),
    TargetLocality(
        "Brookefield",
        search_aliases=(
            "Brookfield Bengaluru",
            "Kundalahalli Brookefield",
        ),
    ),
    TargetLocality("Ulsoor"),
    TargetLocality(
        "Sarjapur Road",
        area_type="corridor",
        search_aliases=(
            "Sarjapura Road",
        ),
    ),
    TargetLocality(
        "Bannerghatta Road",
        area_type="corridor",
        search_aliases=(
            "Bannerghatta Main Road",
        ),
    ),
    TargetLocality(
        "Sadashivanagar",
        search_aliases=(
            "Sadashiva Nagar",
            "Sadashivanagara",
        ),
    ),
)
