from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LocalityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    locality_id: UUID
    name: str


class LocalityListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[LocalityResponse]
    total: int
    limit: int
    offset: int
