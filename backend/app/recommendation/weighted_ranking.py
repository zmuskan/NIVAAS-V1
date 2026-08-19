from backend.app.database import (
    init_pool,
    close_pool,
    get_connection,
)


def get_budget_limit(budget: str) -> int:

    budget_map = {
        "Below 15k": 15000,
        "15k-25k": 25000,
        "25k-40k": 40000,
        "40k+": 100000,
    }

    return budget_map.get(budget, 25000)


def recommend(
    budget: str,
    work: str,
    priority: str,
    lifestyle: str,
):

    budget_limit = get_budget_limit(budget)

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT

                    l.name,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='avg_rent'
                            THEN feature_value
                        END
                    ),0) AS avg_rent,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='listing_count'
                            THEN feature_value
                        END
                    ),0) AS listing_count,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='inventory_score'
                            THEN feature_value
                        END
                    ),0) AS inventory_score,

                    COALESCE(MAX(
                        CASE
                            WHEN feature_name='density_score'
                            THEN feature_value
                        END
                    ),0) AS density_score

                FROM feature_store.locality_feature f

                JOIN core.locality l
                    ON l.locality_id = f.locality_id

                GROUP BY l.name
                """
            )

            rows = cur.fetchall()

    recommendations = []

    for row in rows:

        locality = row[0]

        avg_rent = float(row[1])

        listing_count = float(row[2])

        inventory_score = float(row[3])

        density_score = float(row[4])

        #################################################
        # Budget Fit
        #################################################

        if avg_rent <= budget_limit:

            budget_score = 100

        else:

            difference = avg_rent - budget_limit

            budget_score = max(
                0,
                100 - (difference / budget_limit) * 100,
            )

        #################################################
        # Availability
        #################################################

        availability_score = min(
            listing_count * 5,
            100,
        )

        #################################################
        # Lifestyle
        #################################################

        lifestyle_score = 0

        if lifestyle == "Student":

            lifestyle_score = (
                density_score * 0.70
                + availability_score * 0.30
            )

        elif lifestyle == "Young Professional":

            lifestyle_score = (
                inventory_score * 0.60
                + density_score * 0.40
            )

        elif lifestyle == "Family":

            lifestyle_score = (
                inventory_score * 0.70
                + availability_score * 0.30
            )

        else:

            lifestyle_score = (
                inventory_score * 0.50
                + density_score * 0.50
            )

        #################################################
        # Final Score
        #################################################

        match_score = (
            budget_score * 0.50
            + lifestyle_score * 0.30
            + availability_score * 0.20
        )

        #################################################
        # Reason
        #################################################

        if budget_score > 90:

            reason = "Strong fit for your budget"

        elif availability_score > 70:

            reason = "Large number of available rentals"

        else:

            reason = "Balanced option across multiple factors"

        recommendations.append(
            {
                "locality": locality,

                "match_score": round(
                    match_score,
                    1,
                ),

                "avg_rent": round(avg_rent),

                "listing_count": int(listing_count),

                "budget_fit": round(
                    budget_score,
                    0,
                ),

                "availability_score": round(
                    availability_score,
                    0,
                ),

                "activity_score": round(
                    density_score,
                    0,
                ),

                "reason": reason,
            }
        )

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True,
    )

    return recommendations[:10]


if __name__ == "__main__":

    init_pool()

    try:

        rows = recommend(
            budget="Below 15k",
            work="Whitefield",
            priority="Affordable Rent",
            lifestyle="Student",
        )

        for row in rows:
            print(row)

    finally:

        close_pool()
