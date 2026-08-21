def generate_reasons(
    rent_score: float,
    metro_score: float,
    property_count: float,
):
    reasons = []

    if rent_score >= 90:
        reasons.append("Affordable rent")

    if metro_score >= 50:
        reasons.append("Strong metro access")

    if property_count >= 5:
        reasons.append("High property availability")

    return reasons
