from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locality_id: UUID
    name: str

    listing_count: int

    avg_rent: Decimal | None
    median_rent: Decimal | None
    min_rent: Decimal | None
    max_rent: Decimal | None

    avg_rent_per_sqft: Decimal | None
    avg_area_sqft: Decimal | None
    avg_bhk: Decimal | None

    avg_deposit: Decimal | None
    median_deposit: Decimal | None

    apartment_pct: Decimal | None
    independent_house_pct: Decimal | None
    independent_floor_pct: Decimal | None
    studio_pct: Decimal | None
    villa_pct: Decimal | None

    generated_at: datetime


class AnalyticsListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[AnalyticsResponse]
    total: int
