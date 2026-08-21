export function mapRecommendationToMatch(item: any) {
    return {
        locality: {
            id: item.locality.toLowerCase().replaceAll(" ", "-"),

            name: item.locality,

            district: "Bangalore",

            avgRent: item.avg_rent,

            blurb: item.match_reason,

            listings: item.listing_count,

            availability:
                item.listing_count > 100
                    ? "Very strong"
                    : item.listing_count > 50
                        ? "Strong"
                        : "Steady",

            rentRange: `₹${Number(item.min_rent).toLocaleString()} - ₹${Number(item.max_rent).toLocaleString()}`,

            imagine: [
                "Rental demand remains healthy in this locality."
            ],
        },

        reasons: [
            item.match_reason,
        ],
    };
}
