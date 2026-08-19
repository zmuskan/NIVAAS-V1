from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    budget: str
    work: str
    priority: str
    lifestyle: str


print("SCHEMA LOADED")
