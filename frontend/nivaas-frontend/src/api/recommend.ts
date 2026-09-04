import { mapRecommendationToMatch } from "@/utils/recommendationMapper";

const API_BASE = "https://nivaas-backend.onrender.com";

export async function getRecommendations(answers: any) {
    console.log("ANSWERS", answers);

    const budgetMap: Record<string, number> = {
        upto15: 15000,
        "15to25": 25000,
        "25to40": 40000,
        above40: 50000,
    };

    const requestBody = {
        budget: budgetMap[answers.budget] ?? 25000,

        user_type: answers.lifestyle,

        office_locality: answers.workArea || null,

        prioritize_affordability:
            answers.priorities?.includes("affordable") ?? false,

        prioritize_family:
            answers.priorities?.includes("family") ?? false,

        prioritize_lifestyle:
            answers.priorities?.includes("active") ?? false,

        prioritize_commute:
            Boolean(answers.workArea),
    };

    console.log("REQUEST BODY", requestBody);

    const response = await fetch(
        `${API_BASE}/recommend`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        }
    );

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Backend Error:", errorText);
        throw new Error(errorText);
    }

    const data = await response.json();

    console.log("RESPONSE", data);

    const items =
        data.items ??
        data.recommendations ??
        [];

    return items.map(mapRecommendationToMatch);
}
