from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    rent_weight: float = 0.5
    metro_weight: float = 0.3
    property_weight: float = 0.2
