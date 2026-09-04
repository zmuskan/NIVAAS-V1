import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getLocality } from "../api/locality";
import { LocalityProfile } from "@/components/nivaas/LocalityProfile";
import { NivBot } from "@/components/nivaas/NivBot";

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

                const merged = {
                    id: slug,
                    name: api.name,
                    avgRent: Number(api.avg_rent ?? 0),
                    minRent: Number(api.min_rent ?? 0),
                    maxRent: Number(api.max_rent ?? 0),
                    listingCount: Number(api.listing_count ?? 0),

                    overallScore:
                        api.overall_score !== null &&
                            api.overall_score !== undefined
                            ? Number(api.overall_score)
                            : null,

                    inventoryScore:
                        api.inventory_score !== null &&
                            api.inventory_score !== undefined
                            ? Number(api.inventory_score)
                            : null,

                    densityScore:
                        api.density_score !== null &&
                            api.density_score !== undefined
                            ? Number(api.density_score)
                            : null,

                };

                console.log(
                    "API LOCALITY =",
                    api
                );

                console.log(
                    "MERGED LOCALITY =",
                    merged
                );

                setLocality(merged);
            })
            .catch((err) => {
                console.error(
                    "Failed to load locality:",
                    err
                );
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
        <>
            <LocalityProfile
                locality={locality}
                onBack={() => navigate(-1)}
            />

            <NivBot matches={[]} />
        </>

    );
}
