from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SimilarProperty(BaseModel):

    property_id: UUID

    locality_name: str

    property_type: str

    bhk: int

    area_sqft: Decimal

    rent_amount: Decimal

    similarity_score: float


class SimilarPropertyList(BaseModel):

    items: list[SimilarProperty]

    total: int
