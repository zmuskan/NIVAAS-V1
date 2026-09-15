from pydantic import BaseModel
from typing import List


class NivBotRequest(BaseModel):
    question: str
    locality_name: str = ""
    mode: str = "locality"
    compare_names: List[str] = []


class NivBotResponse(BaseModel):
    answer: str
