from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    min_budget: float
    max_budget: float
    user_type: str | None = None
    office_locality: str | None = None
    prioritize_affordability: bool = False
    prioritize_commute: bool = False
    prioritize_lifestyle: bool = False
    prioritize_family: bool = False
