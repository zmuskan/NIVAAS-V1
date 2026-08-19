import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getRecommendations } from "../api/recommend";

export default function Recommendations() {

    const navigate = useNavigate();

    const [recommendations, setRecommendations] = useState<any[]>([]);

    useEffect(() => {

        const answers = JSON.parse(
            localStorage.getItem("nivaas_answers") || "{}"
        );

        getRecommendations(answers).then((data) => {
            setRecommendations(data);
        });

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
                            "
                        >

                            <div className="flex items-center justify-between">

                                <div>

                                    <h2 className="text-4xl mb-3">
                                        {locality.locality}
                                    </h2>

                                    <p className="text-emerald-300 text-lg">
                                        {locality.match_reason}
                                    </p>
                                </div>

                            </div>


                            <div className="mt-6 space-y-2 text-white/70">

                                <p>
                                    Average Rent:
                                    {" "}
                                    ₹{Number(locality.avg_rent).toLocaleString()}
                                </p>

                                <p>
                                    Rent Range:
                                    {" "}
                                    ₹{Number(locality.min_rent).toLocaleString()}
                                    {" - "}
                                    ₹{Number(locality.max_rent).toLocaleString()}
                                </p>

                                <p>
                                    Listings Available:
                                    {" "}
                                    {locality.listing_count}
                                </p>

                            </div>

                            <button
                                onClick={() =>
                                    navigate(
                                        `/locality/${locality.locality.toLowerCase().replaceAll(" ", "-")}`
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

            </div>

        </div>
    );
}
