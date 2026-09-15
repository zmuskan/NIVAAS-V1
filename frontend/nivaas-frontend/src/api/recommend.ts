import { mapRecommendationToMatch } from "@/utils/recommendationMapper";
import { budgetRanges, type BudgetKey } from "@/data/nivaas";

const API_BASE = "https://nivaas-backend.onrender.com";

export async function getRecommendations(answers: any) {
    const budgetMap: Record<
        BudgetKey,
        { min: number; max: number }
    > = {
        under15: budgetRanges.UNDER_15K,
        "15to25": budgetRanges.BETWEEN_15_25K,
        "25to40": budgetRanges.BETWEEN_25_40K,
        "40to60": budgetRanges.BETWEEN_40_60K,
        "60plus": budgetRanges.ABOVE_60K,
    };

    const selectedBudget =
        budgetMap[answers.budget as BudgetKey] ??
        budgetRanges.BETWEEN_15_25K;

    const requestBody = {
        min_budget: selectedBudget.min,
        max_budget: selectedBudget.max,

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
        throw new Error(errorText);
    }

    const data = await response.json();

    const items =
        data.items ??
        data.recommendations ??
        [];

    return items.map(mapRecommendationToMatch);
}
