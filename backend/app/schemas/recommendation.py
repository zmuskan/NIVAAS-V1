from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class RecommendationResponse(BaseModel):

    property_id: UUID
    locality_id: UUID
    locality_name: str

    property_type: str

    bhk: int

    area_sqft: Decimal

    furnishing_status: str | None

    rent_amount: Decimal

    listing_count: int | None = None

    avg_rent: Decimal | None = None

    avg_rent_per_sqft: Decimal | None = None

    apartment_pct: Decimal | None = None

    independent_house_pct: Decimal | None = None

    villa_pct: Decimal | None = None

    recommendation_score: float


class RecommendationListResponse(BaseModel):

    items: list[RecommendationResponse]
    total: int
