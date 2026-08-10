import { LOCALITIES } from "@/data/localities";

export function getRecommendations(answers: any) {
    return LOCALITIES.map((locality) => {
        let score = 0;

        if (answers.priority === "Nightlife")
            score += locality.nightlife * 10;

        if (answers.priority === "Family Friendly")
            score += locality.family * 10;

        if (answers.priority === "Metro Access")
            score += locality.metro * 10;

        if (answers.work === "Koramangala")
            score += locality.commuteKoramangala * 10;

        if (answers.work === "Whitefield")
            score += locality.commuteWhitefield * 10;

        return {
            ...locality,
            score,
        };
    }).sort((a, b) => b.score - a.score);
}
