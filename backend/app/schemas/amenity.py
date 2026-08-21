from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class AmenityResponse(BaseModel):

    amenity_id: UUID

    locality_id: UUID | None

    amenity_type: str

    name: str | None

    latitude: Decimal

    longitude: Decimal


class AmenityListResponse(BaseModel):

    items: list[AmenityResponse]

    total: int
