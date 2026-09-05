import type { Match } from "@/data/nivaas";

export function mapRecommendationToMatch(item: any): Match {
    return {
        locality: {
            id: item.locality,
            name: item.locality,

            avgRent: item.avg_rent,
            minRent: item.min_rent,
            maxRent: item.max_rent,

            listingCount: item.listing_count,
            highlights: item.highlights ?? [],

            overallScore: item.final_score,
            inventoryScore: item.inventory_score,
            densityScore: item.density_score,
        },

        reasons: item.match_reason
            ? item.match_reason.split(",").map((r: string) => r.trim())
            : [],
    };
}
