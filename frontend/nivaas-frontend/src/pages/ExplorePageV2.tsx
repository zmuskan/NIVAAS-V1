import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getLocality } from "../api/locality";
import { LocalityProfile } from "@/components/nivaas/LocalityProfile";

export default function LocalityProfilePage() {
    const { slug } = useParams();
    const navigate = useNavigate();

    const [mergedLocality, setMergedLocality] = useState<any>(null);

    useEffect(() => {
        if (!slug) return;

        const localityName = slug;

        getLocality(localityName).then((api) => {
            const merged = {
                id: slug,
                name: api.name,
                avgRent: Number(api.avg_rent ?? 0),
                minRent: Number(api.min_rent ?? 0),
                maxRent: Number(api.max_rent ?? 0),
                listingCount: Number(api.listing_count ?? 0),

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
