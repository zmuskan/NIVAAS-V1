from pydantic import BaseModel


class NivBotRequest(BaseModel):
    question: str
    locality_context: str


class NivBotResponse(BaseModel):
    answer: str
