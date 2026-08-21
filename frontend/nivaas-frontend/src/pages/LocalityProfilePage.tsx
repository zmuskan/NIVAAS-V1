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

            const template = localities.find(
                (l) => l.name.toLowerCase() === api.name.toLowerCase()
            );

            console.log("API =", api);
            console.log("TEMPLATE =", template);

            const merged = {
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
