from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    budget: int
    user_type: str
    office_locality: str | None = None
    prioritize_affordability: bool = False
    prioritize_commute: bool = False
    prioritize_lifestyle: bool = False
    prioritize_family: bool = False
