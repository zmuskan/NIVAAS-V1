"""
elt/staging/transformer.py

Transformation layer for the NIVAAS staging pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from elt.staging.validator import safe_float, safe_int, safe_str


@dataclass
class StagingListing:
    raw_listing_id: UUID
    scrape_run_id: Optional[UUID]

    external_listing_id: Optional[str]

    property_type: str
    bhk: int
    bathrooms: Optional[int]

    rent_amount: float
    deposit_amount: Optional[float]
    maintenance_amount: Optional[float]

    furnishing_status: Optional[str]

    area_sqft: float

    locality: str

    latitude: Optional[float]
    longitude: Optional[float]

    listing_url: Optional[str]

    transformed_at: datetime


class ListingTransformer:
    """Transforms a raw payload into a normalized staging record."""

    @classmethod
    def transform(
        cls,
        raw_listing_id: UUID,
        scrape_run_id: Optional[UUID],
        payload: dict[str, Any],
    ) -> StagingListing:

        locality = cls._normalize_plain_string(payload.get("locality"))
        property_type = cls._normalize_upper_string(payload.get("property_type"))
        furnishing_status = cls._normalize_upper_string(payload.get("furnish_type"))

        bhk = safe_int(payload.get("bedroom"))
        bathrooms = safe_int(payload.get("bathroom"))

        area_sqft = safe_float(payload.get("area"))

        rent_amount = safe_float(payload.get("price"))
        deposit_amount = safe_float(payload.get("deposit"))
        maintenance_amount = safe_float(payload.get("maintenance"))

        latitude = safe_float(payload.get("latitude"))
        longitude = safe_float(payload.get("longitude"))

        external_listing_id = cls._normalize_plain_string(
            payload.get("external_listing_id")
        )

        listing_url = cls._normalize_plain_string(
            payload.get("listing_url")
        )

        # Defensive defaults (validator should already enforce these)
        if locality is None:
            locality = ""

        if property_type is None:
            property_type = ""

        if bhk is None:
            bhk = 0

        if area_sqft is None:
            area_sqft = 0.0

        if rent_amount is None:
            rent_amount = 0.0

        return StagingListing(
            raw_listing_id=raw_listing_id,
            scrape_run_id=scrape_run_id,
            external_listing_id=external_listing_id,
            property_type=property_type,
            bhk=bhk,
            bathrooms=bathrooms,
            rent_amount=rent_amount,
            deposit_amount=deposit_amount,
            maintenance_amount=maintenance_amount,
            furnishing_status=furnishing_status,
            area_sqft=area_sqft,
            locality=locality,
            latitude=latitude,
            longitude=longitude,
            listing_url=listing_url,
            transformed_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _normalize_plain_string(value: Any) -> Optional[str]:
        return safe_str(value)

    @staticmethod
    def _normalize_upper_string(value: Any) -> Optional[str]:
        value = safe_str(value)
        if value is None:
            return None
        return value.upper()
