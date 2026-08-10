import { useNavigate } from "react-router-dom";
import { getRecommendations } from "@/utils/recommend";

export default function Recommendations() {
    const navigate = useNavigate();

    const answers = JSON.parse(
        localStorage.getItem("nivaas_answers") || "{}"
    );

    const recommendations = getRecommendations(answers);

    return (
        <div className="min-h-screen text-white px-6 py-20">
            <div className="mx-auto max-w-5xl">

                <h1 className="font-serif text-6xl mb-4">
                    Your Matches
                </h1>

                <p className="text-white/60 mb-12">
                    Based on what you told Niv.
                </p>

                <div className="space-y-6">
                    {recommendations.map((locality) => (
                        <div
                            key={locality.slug}
                            className="
                rounded-3xl
                border border-white/10
                bg-white/5
                backdrop-blur-xl
                p-8
                transition
                hover:bg-white/10
              "
                        >
                            <div className="flex items-start justify-between">
                                <div>
                                    <h2 className="font-serif text-4xl mb-2">
                                        {locality.name}
                                    </h2>

                                    <p className="text-emerald-300 mb-4">
                                        Lifestyle Match: {locality.score}%
                                    </p>

                                    <div className="space-y-2 text-white/70">
                                        <p>{locality.rent}</p>
                                        <p>{locality.metro} to metro</p>
                                        <p>{locality.vibe}</p>
                                    </div>
                                </div>

                                <button
                                    onClick={() =>
                                        navigate(`/locality/${locality.slug}`)
                                    }
                                    className="
                    rounded-full
                    border
                    border-white/20
                    px-6
                    py-3
                    hover:bg-white
                    hover:text-black
                    transition
                  "
                                >
                                    View Profile
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    );
}
