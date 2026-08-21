import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getLocality } from "../api/locality";
import { LocalityProfile } from "@/components/nivaas/LocalityProfile";
import { localities } from "@/data/nivaas";

export default function LocalityProfilePage() {
    const { slug } = useParams();
    const navigate = useNavigate();

    const [locality, setLocality] = useState<any>(null);

    useEffect(() => {
        if (!slug) return;

        getLocality(slug)
            .then((api) => {
                if (!api?.name) {
                    console.error("Locality not found");
                    return;
                }

                const template = localities.find(
                    (l) =>
                        l.name?.toLowerCase() ===
                        api.name?.toLowerCase()
                );

                const merged = {
                    name: api.name,
                    district: "Bangalore",

                    longBlurb: `${api.name} is a locality in Bangalore.`,

                    availability: "Available",

                    propertyTypes: [],
                    furnishing: [],
                    bhkMix: [],

                    nearby: [],

                    clusters: [],

                    coords: {
                        x: 50,
                        y: 50,
                    },

                    dayInLife: {
                        morning: "Data coming soon.",
                        workday: "Data coming soon.",
                        evening: "Data coming soon.",
                        weekend: "Data coming soon.",
                    },

                    imagine: [],

                    ...template,

                    avgRent: Number(api.avg_rent ?? 0),
                    listings: Number(api.listing_count ?? 0),

                    overallScore: Number(api.overall_score ?? 0),
                    inventoryScore: Number(api.inventory_score ?? 0),
                    densityScore: Number(api.density_score ?? 0),

                    rentRange:
                        api.min_rent && api.max_rent
                            ? `₹${Number(api.min_rent).toLocaleString(
                                "en-IN"
                            )} – ₹${Number(api.max_rent).toLocaleString(
                                "en-IN"
                            )}`
                            : "N/A",
                };

                setLocality(merged);
            })
            .catch((err) => {
                console.error(err);
            });
    }, [slug]);

    if (!locality) {
        return (
            <div className="min-h-screen flex items-center justify-center text-white">
                Loading...
            </div>
        );
    }

    return (
        <LocalityProfile
            locality={locality}
            onBack={() => navigate(-1)}
        />
    );
}
