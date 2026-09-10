import re

from backend.app.repositories.nivbot_repository import NivBotRepository


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

        if "pros" in lowered_question or "cons" in lowered_question:
            pros = []
            cons = []

            if rent_score >= 70:
                pros.append("Relatively affordable rents")
            elif rent_score <= 40:
                cons.append("Higher rental costs")

            if inventory_score >= 70:
                pros.append("Good housing availability")
            elif inventory_score <= 40:
                cons.append("Limited housing inventory")

            if density_score <= 40:
                pros.append("Less crowded environment")
            elif density_score >= 70:
                cons.append("Can feel crowded")

            if overall_score >= 70:
                pros.append("Strong overall locality performance")
            elif overall_score <= 40:
                cons.append("Below-average overall locality score")

            if not pros:
                pros.append("Moderate rental market conditions")

            if not cons:
                cons.append("No major weaknesses identified from available data")

            return (
                f"Pros of {name}: " + ", ".join(pros) +
                ". Cons: " + ", ".join(cons) + "."
            )

        if "overall" in lowered_question or "score" in lowered_question:
            if overall_score >= 75:
                verdict = "one of the stronger-performing localities"
            elif overall_score >= 50:
                verdict = "a moderately performing locality"
            else:
                verdict = "a below-average locality based on current metrics"

            return (
                f"{name} is {verdict}. "
                f"It has an overall score of {overall_score:.0f}, "
                f"average rent of ₹{avg_rent:,.0f}, "
                f"and {listing_count:.0f} active listings."
            )

        if "recommended" in lowered_question or "why" in lowered_question:
            return (
                f"{name} is evaluated using rental affordability, "
                f"housing availability, density, and overall locality metrics. "
                f"It currently has an overall score of {overall_score:.0f}, "
                f"rent score of {rent_score:.0f}, "
                f"and inventory score of {inventory_score:.0f}."
            )

        if any(word in lowered_question for word in ("quiet", "peaceful", "calm")):
            if density_score <= 40:
                return (
                    f"{name} appears relatively peaceful based on its "
                    f"density score of {density_score:.0f}."
                )

            if density_score <= 70:
                return (
                    f"{name} has moderate activity levels with a "
                    f"density score of {density_score:.0f}."
                )

            return (
                f"{name} may feel busy or crowded based on its "
                f"density score of {density_score:.0f}."
            )

        return (
            f"{name} has an overall score of {overall_score:.0f}, "
            f"average rent of ₹{avg_rent:,.0f}, "
            f"inventory score of {inventory_score:.0f}, "
            f"and {listing_count:.0f} active listings. "
            f"Try asking about affordability, density, availability, "
            f"pros and cons, or locality scores."
        )
