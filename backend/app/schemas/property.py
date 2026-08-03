from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PropertyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    property_id: UUID
    locality_id: UUID
    locality_name: str

    property_type: str

    bhk: int
    bathrooms: int | None

    area_sqft: Decimal

    furnishing_status: str | None

    latitude: Decimal
    longitude: Decimal

    listing_id: UUID

    rent_amount: Decimal
    deposit_amount: Decimal | None
    maintenance_amount: Decimal | None

    listing_status: str

    title: str | None
    description: str | None
    listing_url: str | None


class PropertyListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[PropertyResponse]
    total: int
