from pydantic import BaseModel


class LocalityRecommendationResponse(BaseModel):

    locality: str

    min_rent: float

    avg_rent: float

    max_rent: float

    listing_count: int

    match_reason: str


class LocalityRecommendationListResponse(BaseModel):

    items: list[LocalityRecommendationResponse]

    total: int
