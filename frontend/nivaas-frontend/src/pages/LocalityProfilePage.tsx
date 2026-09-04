import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getLocality } from "../api/locality";
import { LocalityProfile } from "@/components/nivaas/LocalityProfile";
import { localities } from "@/data/nivaas";
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

                const template = localities.find(
                    (l) =>
                        l.name?.toLowerCase() ===
                        api.name?.toLowerCase()
                );

                const merged = {
                    ...template,

                    name: api.name,

                    district:
                        template?.district ?? "Bangalore",

                    longBlurb:
                        template?.longBlurb ??
                        `${api.name} is a locality in Bangalore.`,

                    availability:
                        template?.availability ?? "Available",

                    propertyTypes:
                        template?.propertyTypes ?? [],

                    furnishing:
                        template?.furnishing ?? [],

                    bhkMix:
                        template?.bhkMix ?? [],

                    nearby:
                        template?.nearby ?? [],

                    clusters:
                        template?.clusters ?? [],

                    coords:
                        template?.coords ?? {
                            x: 50,
                            y: 50,
                        },

                    dayInLife: template?.dayInLife ?? null,

                    imagine:
                        template?.imagine ?? [],

                    // --------------------------------
                    // API / DATABASE VALUES
                    // --------------------------------

                    avgRent: Number(
                        api.avg_rent ?? 0
                    ),

                    listings: Number(
                        api.listing_count ?? 0
                    ),

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

                    rentRange:
                        api.min_rent !== null &&
                            api.min_rent !== undefined &&
                            api.max_rent !== null &&
                            api.max_rent !== undefined
                            ? `₹${Number(
                                api.min_rent
                            ).toLocaleString(
                                "en-IN"
                            )} – ₹${Number(
                                api.max_rent
                            ).toLocaleString(
                                "en-IN"
                            )}`
                            : "N/A",
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
