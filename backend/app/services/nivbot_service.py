import asyncio
import re

from google import genai
from google.genai import types

from backend.app.config import settings
from backend.app.repositories.nivbot_repository import NivBotRepository


client = genai.Client(api_key=settings.GEMINI_API_KEY)

GEMINI_TIMEOUT_SECONDS = 15
MIN_VALID_ANSWER_LENGTH = 3  # guards against stray 1-word / truncated replies


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

        # --- Repository fetch + parsing is now guarded ---
        try:
            locality = NivBotRepository.get_locality_context(locality_name)
        except Exception as error:
            print(f"NIVBOT REPOSITORY ERROR: {error}")
            return "I'm having trouble reading locality data right now. Please try again in a moment."

        if not locality:
            return f"I couldn't find data for {locality_name}."

        try:
            name = locality[0]
            avg_rent = _number(locality[1])
            listing_count = _number(locality[2])
            inventory_score = _number(locality[3])
            density_score = _number(locality[4])
            overall_score = _number(locality[5])
            rent_score = _number(locality[6])
        except (IndexError, TypeError) as error:
            print(f"NIVBOT DATA SHAPE ERROR: {error}")
            return f"I couldn't fully read the data for {locality_name}. Please try again."

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

- Be professional and concise.
- Do not use greetings, slang, filler, or invented information.
- If the answer is not available in the data, clearly say that the locality data does not contain that information.
- No markdown, headings, or bullet points.

Locality Data:
{context}

Question:
{question}
"""

        max_attempts = 1
        quota_error = False

        for attempt in range(1, max_attempts + 1):
            try:
                # generate_content is a blocking/synchronous call. Running it directly
                # inside this async function would stall the entire event loop for
                # every other request while Gemini responds. Push it to a thread and
                # bound it with a timeout so a slow/hanging call can't freeze the API.
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        client.models.generate_content,
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            max_output_tokens=120,
                            temperature=0.3,
                            thinking_config=types.ThinkingConfig(thinking_budget=0),
                        ),
                    ),
                    timeout=GEMINI_TIMEOUT_SECONDS,
                )

                answer = (response.text or "").strip() if response else ""

                if len(answer) >= MIN_VALID_ANSWER_LENGTH:
                    return answer

                raise ValueError(f"Gemini returned an unusable response: {answer!r}")

            except asyncio.TimeoutError:
                print("GEMINI ERROR: request timed out")
                break  # timeouts aren't worth retrying within the same request

            except Exception as error:
                error_text = str(error)
                is_quota_error = "429" in error_text or "RESOURCE_EXHAUSTED" in error_text

                if is_quota_error:
                    quota_error = True
                    print(f"GEMINI QUOTA ERROR (attempt {attempt}/{max_attempts}): {error_text}")
                else:
                    print(f"GEMINI ERROR: {error_text}")
                    break  # non-quota errors: no point retrying, go straight to fallback

                break  # out of retries

        fallback = NivBotService._fallback_answer(
            question,
            name,
            avg_rent,
            listing_count,
            inventory_score,
            density_score,
            overall_score,
            rent_score,
        )

        if quota_error:
            return (
                "NivBot is currently busy because the AI quota has been reached. "
                "Here's what I can tell from the available locality data: "
                + fallback
            )

        return fallback

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
        question_words = set(re.findall(r"[a-z]+", lowered_question))

        if (
            question_words.intersection({"hi", "hello", "hey"})
            or "good morning" in lowered_question
            or "good evening" in lowered_question
        ):
            return (
                f"I'm NivBot. I can help with rent, affordability, "
                f"crowding and listing availability for {name}."
            )

        if question_words.intersection({
            "owner",
            "landlord",
            "aqi",
            "pollution",
            "crime",
            "safety",
            "water",
            "metro",
            "traffic",
        }):
            return (
                f"I don't currently have {name} data for that. "
                f"I can answer questions about rent, affordability, "
                f"crowding and listing availability."
            )

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
