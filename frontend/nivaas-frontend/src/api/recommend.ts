import { mapRecommendationToMatch } from "@/utils/recommendationMapper";

const API_BASE = "https://nivaas-backend.onrender.com";

export async function getRecommendations(answers: any) {
    console.log("ANSWERS", answers);

const payload = {
    budget: answers.budget,
    work: answers.workArea,
    priority: answers.priorities,
    lifestyle: answers.lifestyle,
};

console.log("PAYLOAD", payload);

    const response = await fetch(
        `${API_BASE}/recommend`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                budget: answers.budget,
                work: answers.workArea,
                priority: answers.priorities.join(", "),
                lifestyle: answers.lifestyle,
            }),
        }
    );

    const data = await response.json();

    const items =
        data.items ??
        data.recommendations ??
        [];

    return items.map(mapRecommendationToMatch);
}
