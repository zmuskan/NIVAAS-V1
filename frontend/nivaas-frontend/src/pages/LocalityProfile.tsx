import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getLocality } from "../api/locality";

export default function LocalityProfile() {

    const { slug } = useParams();

    const [data, setData] = useState<any>(null);

    useEffect(() => {

        if (!slug) return;

        const localityName =
            slug.replaceAll("-", " ");

        getLocality(localityName)
            .then((result) => {
                setData(result);
            });

    }, [slug]);

    if (!data) {
        return (
            <div className="min-h-screen flex items-center justify-center text-white">
                Loading...
            </div>
        );
    }

    return (
        <div className="min-h-screen text-white px-6 py-20">

            <div className="mx-auto max-w-6xl">

                <h1 className="font-serif text-6xl mb-4">
                    {data.name}
                </h1>

                <p className="text-emerald-300 text-2xl mb-10">
                    NIVAAS Match Score: {Number(data.overall_score).toFixed(1)}
                </p>

                <div className="grid md:grid-cols-4 gap-6">

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3 className="text-white/60 mb-2">
                            Average Rent
                        </h3>

                        <p className="text-3xl">
                            ₹{Number(data.avg_rent).toLocaleString()}
                        </p>
                    </div>

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3 className="text-white/60 mb-2">
                            Listings
                        </h3>

                        <p className="text-3xl">
                            {data.listing_count}
                        </p>
                    </div>

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3 className="text-white/60 mb-2">
                            Availability
                        </h3>

                        <p className="text-3xl">
                            {Number(data.inventory_score).toFixed(0)}
                        </p>
                    </div>

                    <div className="rounded-3xl bg-white/5 p-6">
                        <h3 className="text-white/60 mb-2">
                            Activity Score
                        </h3>

                        <p className="text-3xl">
                            {Number(data.density_score).toFixed(0)}
                        </p>
                    </div>

                </div>

                <div className="mt-10 rounded-3xl bg-white/5 p-8">

                    <h2 className="text-3xl mb-6">
                        Locality Intelligence
                    </h2>

                    <div className="space-y-3 text-lg">

                        <p>
                            Match Score:
                            {" "}
                            <span className="text-emerald-300">
                                {Number(data.overall_score).toFixed(1)}
                            </span>
                        </p>

                        <p>
                            Rental Availability:
                            {" "}
                            {Number(data.inventory_score).toFixed(1)}
                        </p>

                        <p>
                            Area Activity:
                            {" "}
                            {Number(data.density_score).toFixed(1)}
                        </p>

                        <p>
                            Rent Range:
                            {" "}
                            ₹{Number(data.min_rent).toLocaleString()}
                            {" - "}
                            ₹{Number(data.max_rent).toLocaleString()}
                        </p>

                        <p>
                            Property Count:
                            {" "}
                            {data.property_count}
                        </p>

                    </div>

                </div>

            </div>

        </div>
    );
}
