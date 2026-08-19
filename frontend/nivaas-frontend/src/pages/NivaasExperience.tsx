import { useMemo, useState } from "react";

import { Journey } from "@/components/nivaas/Journey";
import { Results } from "@/components/nivaas/Results";
import { LocalityProfile } from "@/components/nivaas/LocalityProfile";
import { NivBot } from "@/components/nivaas/NivBot";

import {
    rankLocalities,
    type Answers,
    type Locality,
} from "@/data/nivaas";

type Stage = "journey" | "results" | "profile";

export default function NivaasExperience() {
    const [stage, setStage] = useState<Stage>("journey");

    const [answers, setAnswers] =
        useState<Answers>({
            name: "",
            priorities: [],
        });

    const [locality, setLocality] =
        useState<Locality | null>(null);

    const matches = useMemo(
        () =>
            stage === "journey"
                ? []
                : rankLocalities(answers),
        [stage, answers]
    );

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
                    onSelect={(l) => {
                        setLocality(l);
                        setStage("profile");
                    }}
                    onRestart={() => {
                        setAnswers({
                            name: "",
                            priorities: [],
                        });
                        setLocality(null);
                        setStage("journey");
                    }}
                />
            )}

            {stage === "profile" && locality && (
                <LocalityProfile
                    locality={locality}
                    onBack={() => {
                        setStage("results");
                    }}
                />
            )}

            {stage !== "journey" && (
                <NivBot matches={matches} />
            )}
        </main>
    );
}
