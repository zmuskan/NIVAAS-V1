"""
elt/core/matcher.py

Property matching layer for the NIVAAS core pipeline.

Property Matching v1 (deterministic, non-fuzzy):
    property_hash = SHA256(locality | property_type | bhk | area_sqft)

If a property with this exact hash already exists in core.property,
its property_id is reused. Otherwise a new property is created.

This module does NOT perform database I/O. It is a pure computation
layer: given normalized staging fields, it produces a deterministic
hash and a structured "match key" that the repository layer uses to
look up or insert into core.property.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Optional


def _normalize_component(value: Optional[str]) -> str:
    """Lowercase and trim a string component for stable hashing."""
    if value is None:
        return ""
    return value.strip().lower()


def _normalize_numeric_component(value: Optional[float]) -> str:
    """
    Format a numeric component deterministically for stable hashing.

    Uses a fixed-precision representation so that floating point
    formatting differences (e.g. 1200.0 vs 1200) do not produce
    different hashes for the same logical value.
    """
    if value is None:
        return ""
    return f"{float(value):.2f}"


def _normalize_int_component(value: Optional[int]) -> str:
    if value is None:
        return ""
    return str(int(value))


@dataclass(frozen=True)
class PropertyMatchKey:
    """
    Canonical, normalized identity of a property used for deduplication.

    Two staging_listing rows that resolve to the same PropertyMatchKey
    are considered the same physical property under matching v1.
    """

    locality: str
    property_type: str
    bhk: int
    area_sqft: float

    def normalized_locality(self) -> str:
        return _normalize_component(self.locality)

    def normalized_property_type(self) -> str:
        return _normalize_component(self.property_type)

    def normalized_bhk(self) -> str:
        return _normalize_int_component(self.bhk)

    def normalized_area_sqft(self) -> str:
        return _normalize_numeric_component(self.area_sqft)

    def canonical_string(self) -> str:
        return "|".join(
            [
                self.normalized_locality(),
                self.normalized_property_type(),
                self.normalized_bhk(),
                self.normalized_area_sqft(),
            ]
        )

    def property_hash(self) -> str:
        canonical = self.canonical_string()
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class PropertyMatcher:
    """Computes deterministic property match keys and hashes from staging data."""

    @staticmethod
    def build_match_key(
        locality: str,
        property_type: str,
        bhk: int,
        area_sqft: float,
    ) -> PropertyMatchKey:
        return PropertyMatchKey(
            locality=locality,
            property_type=property_type,
            bhk=bhk,
            area_sqft=area_sqft,
        )

    @classmethod
    def compute_hash(
        cls,
        locality: str,
        property_type: str,
        bhk: int,
        area_sqft: float,
    ) -> str:
        match_key = cls.build_match_key(
            locality=locality,
            property_type=property_type,
            bhk=bhk,
            area_sqft=area_sqft,
        )
        return match_key.property_hash()
