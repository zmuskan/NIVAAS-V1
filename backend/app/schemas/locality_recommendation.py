from pydantic import BaseModel


class LocalityRecommendationResponse(BaseModel):

    locality: str

    min_rent: float

    avg_rent: float

    max_rent: float

    listing_count: int

    inventory_score: float

    density_score: float

    final_score: float

    student_score: float

    family_score: float

    rent_score: float

    match_reason: str

    affordability_score: float

    commute_bonus: float

    similarity_score: float


class LocalityRecommendationListResponse(BaseModel):

    items: list[LocalityRecommendationResponse]

    total: int
