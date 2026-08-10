import { useState } from "react";
import { useNavigate } from "react-router-dom";

const QUESTIONS = [
    {
        key: "budget",
        text: "What's your monthly rent budget?",
        options: ["<15k", "15k-25k", "25k-40k", "40k+"],
    },
    {
        key: "work",
        text: "Where do you work?",
        options: [
            "Whitefield",
            "Koramangala",
            "Electronic City",
            "Hebbal",
            "Remote",
        ],
    },
    {
        key: "priority",
        text: "What matters most to you?",
        options: [
            "Short Commute",
            "Nightlife",
            "Affordable Rent",
            "Metro Access",
            "Safety",
        ],
    },
    {
        key: "lifestyle",
        text: "Which describes you best?",
        options: [
            "Student",
            "Young Professional",
            "Couple",
            "Family",
        ],
    },
];

export default function NivChat() {
    const navigate = useNavigate();

    const [step, setStep] = useState(0);

    const [answers, setAnswers] = useState<any>({});

    const question = QUESTIONS[step];

    const choose = (value: string) => {
        const updated = {
            ...answers,
            [question.key]: value,
        };

        setAnswers(updated);

        if (step === QUESTIONS.length - 1) {
            localStorage.setItem(
                "nivaas_answers",
                JSON.stringify(updated)
            );

            navigate("/recommendations");
            return;
        }

        setStep(step + 1);
    };

    return (
        <div className="flex min-h-screen items-center justify-center px-6">
            <div className="w-full max-w-2xl">

                <div className="mb-8">
                    <div className="inline-flex rounded-full bg-emerald-500/20 px-4 py-2 text-sm text-emerald-300">
                        Niv
                    </div>
                </div>

                <h1 className="mb-10 text-4xl font-light leading-tight">
                    {question.text}
                </h1>

                <div className="flex flex-wrap gap-4">
                    {question.options.map((option) => (
                        <button
                            key={option}
                            onClick={() => choose(option)}
                            className="rounded-full border border-white/20 px-6 py-3 transition hover:bg-white hover:text-black"
                        >
                            {option}
                        </button>
                    ))}
                </div>

            </div>
        </div>
    );
}
