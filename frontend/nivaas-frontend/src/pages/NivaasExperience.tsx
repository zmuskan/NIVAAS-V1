import { Journey } from "@/components/nivaas/Journey";
import { Results } from "@/components/nivaas/Results";
import { NivBot } from "@/components/nivaas/NivBot";
import { useEffect, useState } from "react";
import { getRecommendations } from "@/api/recommend";
import type { Answers } from "@/data/nivaas";

type Stage = "journey" | "results";

export default function NivaasExperience() {
    const [stage, setStage] = useState<Stage>("journey");

    const [answers, setAnswers] = useState<Answers>({
        name: "",
        priorities: [],
    });

    const [matches, setMatches] = useState<any[]>([]);

    useEffect(() => {
        if (stage !== "results") return;

        getRecommendations(answers)
            .then((data) => {
                setMatches(data);
            })
            .catch(console.error);
    }, [stage, answers]);

    return (
        <main className="min-h-screen bg-background">
            {stage === "journey" && (
                <Journey
                    onComplete={(a) => {
                        setAnswers(a);
                        setStage("results");
                    }}
                />
            )}

            {stage === "results" && (
                <Results
                    answers={answers}
                    matches={matches}
                    onRestart={() => {
                        setAnswers({
                            name: "",
                            priorities: [],
                        });

                        setStage("journey");
                    }}
                />
            )}

            {stage !== "journey" && (
                <NivBot matches={matches} />
            )}
        </main>
    );
}
