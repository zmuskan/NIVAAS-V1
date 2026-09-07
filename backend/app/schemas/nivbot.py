from pydantic import BaseModel


class NivBotRequest(BaseModel):
    question: str
    locality_name: str


class NivBotResponse(BaseModel):
    answer: str
