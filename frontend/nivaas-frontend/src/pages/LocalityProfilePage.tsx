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

        getLocality(slug).then((api) => {

            if (!api.name) {
                console.error("Locality not found:", slug);
                return;
            }

            const template = localities.find(
                (l) =>
                    l.name.toLowerCase() ===
                    api.name.toLowerCase()
            );

            console.log("API =", api);
            console.log("TEMPLATE =", template);

            const merged = {
            name: api.name,
            district: "Bangalore",
            longBlurb: "Locality profile coming soon.",
            availability: "Steady",

            propertyTypes: [],
            furnishing: [],
            bhkMix: [],

            nearby: [],

            dayInLife: {
                morning: "Data coming soon.",
                workday: "Data coming soon.",
                evening: "Data coming soon.",
                weekend: "Data coming soon.",
            },

            imagine: [],

            ...template,

                avgRent: api.avg_rent,
                listings: api.listing_count,

                rentRange:
                    api.min_rent && api.max_rent
                        ? `₹${api.min_rent.toLocaleString()} – ₹${api.max_rent.toLocaleString()}`
                        : "N/A",
            };

            console.log("MERGED =", merged);

            setLocality(merged);
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
