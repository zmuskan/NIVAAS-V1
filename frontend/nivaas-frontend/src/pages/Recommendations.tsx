import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getRecommendations } from "../api/recommend";

export default function Recommendations() {

    const navigate = useNavigate();

    const [recommendations, setRecommendations] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {

        const answers = JSON.parse(
            localStorage.getItem("nivaas_answers") || "{}"
        );

        getRecommendations(answers).then((data) => {
            setRecommendations(data);
        }).finally(() => setIsLoading(false));

    }, []);

    return (
        <div className="min-h-screen text-white px-6 py-20">

            <div className="mx-auto max-w-6xl">

                <h1 className="font-serif text-6xl mb-4">
                    Your Matches
                </h1>

                <p className="text-white/60 mb-12">
                    Ranked based on your budget, lifestyle and preferences.
                </p>

                {isLoading ? (
                    <div className="flex min-h-64 flex-col items-center justify-center text-center">
                        <div className="size-10 animate-spin rounded-full border-2 border-white/15 border-t-emerald-300" />
                        <p className="mt-5 text-sm text-white/60">Finding neighbourhoods that fit</p>
                    </div>
                ) : recommendations.length === 0 ? (
                    <div className="rounded-3xl border border-white/10 bg-white/5 p-8 text-center">
                        <h2 className="text-2xl">No localities matched your current criteria.</h2>
                        <p className="mt-3 text-white/60">
                            Try adjusting your budget range or preferences to explore more options.
                        </p>
                    </div>
                ) : (
                    <div className="space-y-8">

                        {recommendations.slice(0, 5).map((locality) => (

                            <div
                                key={locality.locality}
                                className="
                                rounded-3xl
                                border border-white/10
                                bg-white/5
                                backdrop-blur-xl
                                p-8
                                transition-all duration-300 hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.08]
                            "
                            >

                                <div className="flex items-center justify-between">

                                    <div>

                                        <h2 className="text-4xl mb-3">
                                            {locality.locality.name}
                                        </h2>

                                        <p className="text-emerald-300 text-lg">
                                            {locality.reasons[0] ?? "Recommended based on your preferences."}
                                        </p>
                                    </div>

                                </div>


                                <div className="mt-6 space-y-2 text-white/70">

                                    <p>
                                        Average Rent:
                                        {" "}
                                        ₹{Number(locality.locality.avgRent).toLocaleString()}
                                    </p>

                                    <p>
                                        Rent Range:
                                        {" "}
                                        ₹{Number(locality.locality.minRent).toLocaleString()}
                                        {" - "}
                                        ₹{Number(locality.locality.maxRent).toLocaleString()}
                                    </p>

                                    <p>
                                        Listings Available:
                                        {" "}
                                        {locality.locality.listingCount}
                                    </p>

                                    <p>
                                        Inventory Status:
                                        {" "}
                                        {locality.locality.listingCount < 5 ? "Limited" : "Healthy"}
                                    </p>

                                </div>

                                <button
                                    onClick={() =>
                                        navigate(
                                            `/locality/${locality.locality.name.toLowerCase().replaceAll(" ", "-")}`
                                        )
                                    }
                                    className="
                                    mt-6
                                    rounded-full
                                    border border-white/20
                                    px-6 py-3
                                    hover:bg-white/10
                                    transition
                                "
                                >
                                    View Full Analysis
                                </button>

                            </div>

                        ))}

                    </div>
                )}

            </div>

        </div>
    );
}
