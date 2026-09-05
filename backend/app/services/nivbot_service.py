import google.generativeai as genai
from backend.app.repositories.nivbot_repository import (
    NivBotRepository,
)
from backend.app.config import settings

genai.configure(
    api_key=settings.GEMINI_API_KEY
)


model = genai.GenerativeModel("gemini-3.6-flash")


class NivBotService:

    @staticmethod

    async def chat(question: str, locality_name: str):

        locality = NivBotRepository.get_locality_context(
            locality_name
        )

        context = str(locality)

        prompt = f"""
    You are NivBot.

    Bangalore rental advisor.

    Locality Data:
    {context}

    Question:
    {question}

    Give practical rental advice.
    """

        response = model.generate_content(prompt)

        return response.text

        prompt = f"""
You are NivBot, NIVAAS's Bangalore rental advisor.

Rules:

- Sound like an experienced Bangalore renter.
- Give direct recommendations.
- Use only the provided data.
- Never say "based on the provided context".
- If data is missing, say so naturally.
- Keep answers under 120 words.
- Use bullets when useful.

LOCALITY DATA:
{locality_context}

USER QUESTION:
{question}
"""

        response = model.generate_content(prompt)

        return response.text
class NivBotService:

    @staticmethod
    async def chat(question: str, locality_context: str):

        print("STEP 1")

        prompt = f"""
        Question: {question}
        Context: {locality_context}
        """

        print("STEP 2")

        response = model.generate_content(prompt)

        print("STEP 3")

        return response.text
