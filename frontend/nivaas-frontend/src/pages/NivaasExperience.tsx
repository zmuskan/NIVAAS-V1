import { Journey } from "@/components/nivaas/Journey";
import { Results } from "@/components/nivaas/Results";
import { NivBot } from "@/components/nivaas/NivBot";
import { useEffect, useState } from "react";
import { getRecommendations } from "@/api/recommend";
import type { Answers } from "../data/nivaas";

type Stage = "journey" | "results";

export default function NivaasExperience() {
    const [stage, setStage] = useState<Stage>("journey");

    const [answers, setAnswers] = useState<Answers>({
        name: "",
        priorities: [],
    });

    const [matches, setMatches] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (stage !== "results") return;

        setIsLoading(true);
        getRecommendations(answers)
            .then((data) => {
                setMatches(data);
            })
            .catch(() => setMatches([]))
            .finally(() => setIsLoading(false));
    }, [stage, answers]);

    return (
        <main className="min-h-screen bg-background">
            {stage === "journey" && (
                <Journey
                    onComplete={(a) => {
                        setAnswers(a);
                        setIsLoading(true);
                        setStage("results");
                    }}
                />
            )}

            {stage === "results" && (
                <Results
                    answers={answers}
                    matches={matches}
                    isLoading={isLoading}
                    onRestart={() => {
                        setAnswers({
                            name: "",
                            priorities: [],
                        });
                        setMatches([]);
                        setIsLoading(false);

                        setStage("journey");
                    }}
                />
            )}

            {stage !== "journey" && (
                <NivBot
                    matches={matches}
                    localityName={matches[0]?.locality?.name ?? ""}
                />
            )}
        </main>
    );
}
