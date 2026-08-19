from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LocalityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locality_id: UUID
    name: str

    min_rent: float | None = None
    avg_rent: float | None = None
    max_rent: float | None = None

    listing_count: int | None = None
    property_count: int | None = None

    


class LocalityListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[LocalityResponse]
    total: int
    limit: int
    offset: int
