from google import genai
from google.genai import types

from backend.app.config import settings
from backend.app.repositories.nivbot_repository import NivBotRepository


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _number(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


class NivBotService:
    @staticmethod
    async def chat(question: str, locality_name: str) -> str:
        if not locality_name.strip():
            return "Please open a locality profile first so I can use its rental data."

        locality = NivBotRepository.get_locality_context(locality_name)
        if not locality:
            return f"I couldn't find data for {locality_name}."

        name = locality[0]
        avg_rent = _number(locality[1])
        listing_count = _number(locality[2])
        inventory_score = _number(locality[3])
        density_score = _number(locality[4])
        overall_score = _number(locality[5])
        rent_score = _number(locality[6])

        context = f"""
Locality: {name}
Average Rent: {avg_rent:.0f}
Listing Count: {listing_count:.0f}
Inventory Score: {inventory_score:.0f}
Density Score: {density_score:.0f}
Overall Score: {overall_score:.0f}
Rent Score: {rent_score:.0f}
"""

        prompt = f"""
You are NivBot, the AI housing assistant of NIVAAS.
Answer the question directly using only the locality data below.

Rules:
- Maximum 2 sentences and 60 words.
- Be professional and concise.
- Do not use greetings, slang, filler, or invented information.
- If the answer is not available in the data, say so.
- No markdown, headings, or bullet points.

Locality Data:
{context}

Question:
{question}
"""

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=120,
                    temperature=0.3,
                ),
            )
            if response and response.text:
                return response.text.strip()
            raise ValueError("Gemini returned an empty response")
        except Exception as error:
            print(f"GEMINI ERROR: {error}")
            return NivBotService._fallback_answer(
                question,
                name,
                avg_rent,
                listing_count,
                inventory_score,
                density_score,
                overall_score,
                rent_score,
            )

    @staticmethod
    def _fallback_answer(
        question: str,
        name: str,
        avg_rent: float,
        listing_count: float,
        inventory_score: float,
        density_score: float,
        overall_score: float,
        rent_score: float,
    ) -> str:
        lowered_question = question.lower()

        if any(word in lowered_question for word in ("rent", "price", "cost", "expense")):
            return f"The average rent in {name} is approximately ₹{avg_rent:,.0f}."

        if any(word in lowered_question for word in ("cheap", "affordable", "expensive", "budget")):
            if rent_score >= 75:
                return f"Yes, {name} is relatively affordable, with average rent around ₹{avg_rent:,.0f}."
            if rent_score >= 50:
                return f"{name} is moderately priced, with average rent around ₹{avg_rent:,.0f}."
            return f"{name} is relatively expensive, with average rent around ₹{avg_rent:,.0f}."

        if any(word in lowered_question for word in ("crowded", "busy", "dense", "density")):
            if density_score >= 75:
                return f"{name} appears quite crowded, with a density score of {density_score:.0f}."
            if density_score >= 50:
                return f"{name} has moderate density, with a density score of {density_score:.0f}."
            return f"{name} is relatively less crowded, with a density score of {density_score:.0f}."

        if any(word in lowered_question for word in ("listing", "availability", "available", "inventory")):
            return f"{name} has {listing_count:.0f} active listings and an inventory score of {inventory_score:.0f}."

        return f"{name} has an overall score of {overall_score:.0f}, average rent of ₹{avg_rent:,.0f}, and {listing_count:.0f} active listings."
