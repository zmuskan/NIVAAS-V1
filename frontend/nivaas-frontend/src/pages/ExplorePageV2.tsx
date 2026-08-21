import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getLocality } from "../api/locality";
import { LocalityProfile } from "@/components/nivaas/LocalityProfile";
import { localities } from "@/data/nivaas";

export default function LocalityProfilePage() {
    const { slug } = useParams();
    const navigate = useNavigate();

    const [mergedLocality, setMergedLocality] = useState<any>(null);

    useEffect(() => {
        if (!slug) return;

        console.log("slug:", slug);

        const templateLocality = localities.find(
            (locality) => locality.id === slug
        );

        console.log("template:", templateLocality);

        if (!templateLocality) {
            return;
        }

        const localityName = templateLocality.name;

        console.log("calling api for:", localityName);

        getLocality(localityName).then((api) => {
            console.log("api response:", api);

            const merged = {
                ...templateLocality,

                avgRent: Number(api.avg_rent),

                listings: Number(api.listing_count),

                rentRange: `₹${Number(api.min_rent).toLocaleString()} – ₹${Number(api.max_rent).toLocaleString()}`,
            };

            setMergedLocality(merged);
        });
    }, [slug]);

    if (!mergedLocality) {
        return (
            <div className="min-h-screen flex items-center justify-center text-white">
                Loading...
            </div>
        );
    }

    return (
        <LocalityProfile
            locality={mergedLocality}
            onBack={() => navigate(-1)}
        />
    );
}
