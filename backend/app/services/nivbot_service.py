import re
from typing import Optional, Sequence

from backend.app.repositories.nivbot_repository import NivBotRepository


def _number(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


class LocalityContext:
    """Small typed wrapper so we stop passing 7 positional floats around."""

    __slots__ = (
        "name",
        "avg_rent",
        "listing_count",
        "inventory_score",
        "density_score",
        "overall_score",
        "rent_score",
    )

    def __init__(self, row: Sequence[object]):
        self.name = row[0]
        self.avg_rent = _number(row[1])
        self.listing_count = _number(row[2])
        self.inventory_score = _number(row[3])
        self.density_score = _number(row[4])
        self.overall_score = _number(row[5])
        self.rent_score = _number(row[6])


# ---------------------------------------------------------------------------
# Human-language translation layer
#
# These are the only places raw scores get read. Every one of them returns a
# sentence a renter would actually say out loud — never a number — unless the
# caller explicitly passes `include_number=True` (used when the user asks for
# an exact figure).
# ---------------------------------------------------------------------------

def _rent_language(avg_rent: float) -> str:
    if avg_rent < 15000:
        return f"quite affordable, with rents typically around ₹{avg_rent:,.0f}"
    if avg_rent < 25000:
        return f"fairly average for Bangalore, with rents typically around ₹{avg_rent:,.0f}"
    if avg_rent < 35000:
        return f"in the mid-range rental market, with rents typically around ₹{avg_rent:,.0f}"
    return f"relatively expensive, with rents typically around ₹{avg_rent:,.0f}"


def _availability_language(inventory_score: float, listing_count: float, include_number: bool = False) -> str:
    if inventory_score >= 70:
        phrase = f"there's good availability right now — {listing_count:.0f} active listings, so you'll have options"
    elif inventory_score >= 40:
        phrase = f"availability is moderate — {listing_count:.0f} active listings, not overflowing but workable"
    else:
        phrase = f"availability is fairly limited at the moment — only {listing_count:.0f} active listings, so you may need to move fast or be flexible"
    if include_number:
        phrase += f" (availability score: {inventory_score:.0f}/100)"
    return phrase


def _density_language(density_score: float, include_number: bool = False) -> str:
    if density_score >= 75:
        phrase = "it tends to be busy and lively, with a lot of foot traffic"
    elif density_score >= 50:
        phrase = "it has a fair amount of activity — not too quiet, not overwhelming"
    else:
        phrase = "it's relatively quiet and peaceful"
    if include_number:
        phrase += f" (density score: {density_score:.0f}/100)"
    return phrase


def _overall_language(overall_score: float, include_number: bool = False) -> str:
    if overall_score >= 75:
        phrase = "one of the stronger-performing areas we track"
    elif overall_score >= 50:
        phrase = "a solid, middle-of-the-road choice"
    else:
        phrase = "has a few trade-offs compared with many other recommended areas, mainly around housing availability and overall livability"
    if include_number:
        phrase += f" (overall score: {overall_score:.0f}/100)"
    return phrase


def _affordability_verdict(avg_rent: float) -> str:
    if avg_rent < 15000:
        return "this is one of the more affordable areas to rent in"
    if avg_rent < 30000:
        return "rents are fairly average for Bangalore"
    return "this area is relatively expensive compared to many parts of the city"


def _wants_raw_numbers(question_words: set) -> bool:
    return bool(question_words.intersection({"score", "number", "numbers", "exact", "stats", "data", "metric", "metrics"}))


class NivBotService:
    @staticmethod
    async def chat(
        question: str,
        locality_name: str = "",
        mode: str = "locality",
        compare_names: Optional[Sequence[str]] = None,
    ) -> str:
        """
        mode: "locality"        -> acts as an area advisor for a single locality page
              "recommendation"  -> acts as a comparison/ranking advisor for the
                                    recommendations page

        compare_names: when provided with 2+ names (typically from the
        recommendations page), NivBot switches into comparison mode regardless
        of `mode`, since comparing is the whole point of that flow.
        """
        compare_names = [n.strip() for n in (compare_names or []) if n and n.strip()]

        if len(compare_names) >= 2:
            return await NivBotService._compare(question, compare_names)

        if not locality_name.strip():
            if mode == "recommendation":
                return (
                    "Pick two or more localities and I can compare them for you — "
                    "rent, availability, vibe, and trade-offs."
                )
            return "Please open a locality profile first so I can use its rental data."

        try:
            row = NivBotRepository.get_locality_context(locality_name)
        except Exception as error:
            print(f"NIVBOT REPOSITORY ERROR: {error}")
            return "I'm having trouble reading locality data right now. Please try again in a moment."

        if not row:
            return f"I couldn't find data for {locality_name}."

        try:
            ctx = LocalityContext(row)
        except (IndexError, TypeError) as error:
            print(f"NIVBOT DATA SHAPE ERROR: {error}")
            return f"I couldn't fully read the data for {locality_name}. Please try again."

        if mode == "recommendation":
            return NivBotService._recommendation_answer(question, ctx)
        return NivBotService._locality_answer(question, ctx)

    # ------------------------------------------------------------------
    # Locality page — acts as an area advisor
    # ------------------------------------------------------------------
    @staticmethod
    def _locality_answer(question: str, ctx: LocalityContext) -> str:
        lowered = question.lower()
        words = set(re.findall(r"[a-z]+", lowered))
        show_numbers = _wants_raw_numbers(words)

        if words.intersection({"hi", "hello", "hey"}) or "good morning" in lowered or "good evening" in lowered:
            return (
                f"Hey! I'm NivBot, your advisor for {ctx.name}. "
                f"Ask me about rent, whether it's a good fit for your budget, "
                f"what the neighborhood feels like, or the pros and cons of living here."
            )

        if words.intersection({"owner", "landlord", "aqi", "pollution", "crime", "safety", "water", "metro", "traffic"}):
            return (
                f"I don't have that kind of data for {ctx.name} yet. "
                f"I can help with rent, affordability, how busy the area feels, and listing availability."
            )

        if any(w in lowered for w in ("rent", "price", "cost", "expense")):
            return f"Rent in {ctx.name} is {_rent_language(ctx.avg_rent)}."

        if any(w in lowered for w in ("affordable", "cheap", "budget")):
            return f"{ctx.name} is {_rent_language(ctx.avg_rent)}. In short, {_affordability_verdict(ctx.avg_rent)}."

        if "expensive" in lowered:
            verdict = "Yes" if ctx.avg_rent > 30000 else ("It's in the mid-range" if ctx.avg_rent > 15000 else "No")
            return f"{verdict} — {ctx.name} is {_rent_language(ctx.avg_rent)}."

        if any(w in lowered for w in ("crowded", "busy", "dense", "density", "quiet", "peaceful", "calm", "vibe", "feel")):
            return f"In {ctx.name}, {_density_language(ctx.density_score, show_numbers)}."

        if any(w in lowered for w in ("listing", "availability", "available", "inventory")):
            return f"In {ctx.name}, {_availability_language(ctx.inventory_score, ctx.listing_count, show_numbers)}."

        if words.intersection({"pros", "cons"}):
            return NivBotService._pros_and_cons(ctx)

        if "overall" in lowered or "score" in lowered or "rating" in lowered:
            return (
                f"{ctx.name} isn't among the strongest-rated localities in our database, "
                f"but that doesn't automatically make it a bad place to live. "
                f"Rent is {_rent_language(ctx.avg_rent)}, and "
                f"{_availability_language(ctx.inventory_score, ctx.listing_count)}."
            )

        if "recommended" in lowered or "why" in lowered:
            return (
                f"I look at rent, availability, how busy the area is, and how it performs "
                f"overall. On those fronts, {ctx.name} is {_overall_language(ctx.overall_score)}, "
                f"and {_affordability_verdict(ctx.avg_rent)}."
            )

        if "worth considering" in lowered or "worth it" in lowered or "should i" in lowered:
            if ctx.overall_score >= 70:
                return f"Yes — {ctx.name} is {_overall_language(ctx.overall_score)}, so it's a strong candidate if the rent fits your budget."
            if ctx.overall_score >= 50:
                return f"{ctx.name} is {_overall_language(ctx.overall_score)}. Worth considering, especially if the location works for you."
            return f"{ctx.name} is {_overall_language(ctx.overall_score)}. I'd weigh it carefully against other options before deciding."

        if any(w in lowered for w in ("advice", "tip", "tips", "should", "move")):
            return NivBotService._practical_advice(ctx)

        return (
            f"Here's the quick picture of {ctx.name}: rent is {_rent_language(ctx.avg_rent)}, "
            f"and {_availability_language(ctx.inventory_score, ctx.listing_count)}. "
            f"Ask me about affordability, the neighborhood vibe, pros and cons, or whether it's worth considering."
        )

    @staticmethod
    def _practical_advice(ctx: LocalityContext) -> str:
        tips = []
        if ctx.inventory_score < 40:
            tips.append("listings move fast here, so be ready to decide quickly and have documents in order")
        else:
            tips.append("you'll have some room to compare a few places before deciding")

        if ctx.avg_rent >= 30000:
            tips.append("negotiate on maintenance charges or lock-in period, since base rent is unlikely to move much")
        else:
            tips.append("you likely have some room to negotiate given the overall price band")

        if ctx.density_score >= 75:
            tips.append("visit at peak hours (morning/evening) to get a feel for noise and traffic before signing")

        return f"A few practical tips for {ctx.name}: " + "; ".join(tips) + "."

    # ------------------------------------------------------------------
    # Recommendation page — single-locality framing (used before a
    # comparison is picked, e.g. "why is this ranked here")
    # ------------------------------------------------------------------
    @staticmethod
    def _recommendation_answer(question: str, ctx: LocalityContext) -> str:
        lowered = question.lower()
        words = set(re.findall(r"[a-z]+", lowered))

        if words.intersection({"hi", "hello", "hey"}):
            return (
                f"I'm NivBot. I can explain why {ctx.name} ranked where it did, "
                f"break down its trade-offs, or compare it against another locality — just ask."
            )

        if "why" in lowered or "ranked" in lowered or "rank" in lowered:
            return (
                f"{ctx.name} ranked where it did mainly because it's {_overall_language(ctx.overall_score)}: "
                f"{_affordability_verdict(ctx.avg_rent)}, and "
                f"{_availability_language(ctx.inventory_score, ctx.listing_count)}."
            )

        if "tradeoff" in lowered.replace("-", "") or "trade off" in lowered:
            return NivBotService._pros_and_cons(ctx)

        # fall back to the same locality-advisor behaviour for anything else
        return NivBotService._locality_answer(question, ctx)

    # ------------------------------------------------------------------
    # Comparison mode
    # ------------------------------------------------------------------
    @staticmethod
    async def _compare(question: str, names: Sequence[str]) -> str:
        contexts = []
        missing = []
        for n in names[:3]:  # keep comparisons readable — cap at 3
            try:
                row = NivBotRepository.get_locality_context(n)
            except Exception as error:
                print(f"NIVBOT REPOSITORY ERROR: {error}")
                return "I'm having trouble reading locality data right now. Please try again in a moment."
            if not row:
                missing.append(n)
                continue
            try:
                contexts.append(LocalityContext(row))
            except (IndexError, TypeError) as error:
                print(f"NIVBOT DATA SHAPE ERROR: {error}")
                missing.append(n)

        if missing:
            return f"I couldn't find data for: {', '.join(missing)}."
        if len(contexts) < 2:
            return "I need at least two localities with data to compare."

        cheapest = min(contexts, key=lambda c: c.avg_rent)
        most_available = max(contexts, key=lambda c: c.inventory_score)
        lifestyle_leader = max(contexts, key=lambda c: (c.overall_score, -c.density_score))
        other = next(c for c in contexts if c is not cheapest)
        budget_choice = cheapest.name
        choice_for_options = most_available.name

        if cheapest.avg_rent == other.avg_rent:
            rent_line = "Both localities are in a similar rent band."
        else:
            rent_line = f"{cheapest.name} is cheaper than {other.name}."

        if most_available.inventory_score == min(c.inventory_score for c in contexts):
            availability_line = "Both localities have similar rental availability."
        else:
            availability_line = f"{most_available.name} has better rental availability."

        if budget_choice == choice_for_options:
            verdict_line = f"Choose {budget_choice} if budget and rental choice both matter."
        else:
            verdict_line = (
                f"Choose {budget_choice} if budget matters. "
                f"Choose {choice_for_options} if you want more rental choice."
            )

        lines = [
            " vs ".join(c.name for c in contexts),
            "",
            "Rent:",
            rent_line,
            "",
            "Availability:",
            availability_line,
            "",
            "Lifestyle:",
            f"{lifestyle_leader.name} appears stronger overall for day-to-day living.",
            "",
            "Verdict:",
            verdict_line,
        ]

        return "\n".join(lines)

    @staticmethod
    def _pros_and_cons(ctx: LocalityContext) -> str:
        pros = []
        cons = []

        if ctx.avg_rent < 15000:
            pros.append("rent is relatively easy on the wallet")
        elif ctx.avg_rent < 25000:
            pros.append("rent is fairly average for Bangalore")
        elif ctx.avg_rent < 35000:
            cons.append("rent sits in the mid-range rental market")
        else:
            cons.append("rent is relatively expensive")

        if ctx.inventory_score >= 70:
            pros.append("plenty of listings to choose from")
        elif ctx.inventory_score <= 40:
            cons.append("listings are limited, so options move fast")

        if ctx.density_score <= 40:
            pros.append("quiet, low-traffic surroundings")
        elif ctx.density_score >= 70:
            cons.append("can feel busy and crowded")

        if ctx.overall_score >= 70:
            pros.append("performs strongly overall compared to other areas")
        elif ctx.overall_score <= 40:
            cons.append("trails other areas on overall performance")

        if not pros:
            pros.append("fairly balanced rental market conditions")
        if not cons:
            cons.append("no major downsides stand out in the data")

        return (
            f"For {ctx.name} — what's working: " + "; ".join(pros) + ". "
            f"What to watch for: " + "; ".join(cons) + ". "
            f"Overall, {ctx.name} works best for people who prioritize proximity to tech parks "
            f"and don't mind having fewer rental options."
        )
