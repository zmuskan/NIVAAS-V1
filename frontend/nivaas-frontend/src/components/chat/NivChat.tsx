import { useState, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";

const QUESTIONS = [
    {
        key: "budget",
        text: "What monthly rent feels comfortable?",
        options: [
            "Under ₹15k",
            "₹15k – ₹25k",
            "₹25k – ₹40k",
            "₹40k – ₹60k",
            "₹60k+",
        ],
    },

    {
        key: "work",
        text: "Where do you spend most weekdays?",
        options: [],
    },

    {
        key: "priority",
        text: "What's most important when choosing a neighbourhood?",
        options: [
            "Affordable Rent",
            "Short Commute",
            "Safety",
            "Metro Access",
            "Rental Availability",
            "Quiet Neighbourhood",
        ],
    },

    {
        key: "lifestyle",
        text: "Who are you moving with?",
        options: [
            "Student",
            "Professional",
            "Couple",
            "Family",
        ],
    },
];

export default function NivChat() {

    const navigate = useNavigate();

    const [step, setStep] = useState(0);

    const [answers, setAnswers] = useState<any>({});
    const [workArea, setWorkArea] = useState("");
    const [selectedPriorities, setSelectedPriorities] = useState<string[]>([]);

    const question = QUESTIONS[step];

    if (!question) {
        return null;
    }

    const choose = (value: string) => {

        if (question.key === "priority") {

            const updated = selectedPriorities.includes(value)
                ? selectedPriorities.filter((p) => p !== value)
                : [...selectedPriorities, value];

            if (updated.length > 2) {
                return;
            }

            setSelectedPriorities(updated);

            if (updated.length === 2) {

                const finalAnswers = {
                    ...answers,
                    priority: updated,
                };

                setAnswers(finalAnswers);

                setTimeout(() => {
                    setStep(step + 1);
                }, 300);
            }

            return;
        }

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

            <div className="w-full max-w-3xl">

                <div className="mb-6">

                    <div
                        className="
                        inline-flex
                        rounded-full
                        bg-emerald-500/10
                        border
                        border-emerald-400/20
                        px-4
                        py-2
                        text-sm
                        text-emerald-300
                        backdrop-blur-md
                        "
                    >
                        NIVAAS AI
                    </div>

                </div>

                <div className="mb-8 text-sm text-white/40">
                    Question {step + 1} of {QUESTIONS.length}
                </div>

                <h1 className="mb-10 text-5xl font-light leading-tight text-white">
                    {question.text}
                </h1>

                {question.key === "work" ? (

                    <div className="space-y-5">

                        <p className="text-sm text-white/50">
                            Office, college, tech park or any area you visit regularly.
                        </p>

                        <input
                            value={workArea}
                            onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                setWorkArea(e.target.value)
                            }
                            placeholder="Whitefield, Manyata Tech Park, Electronic City, Remote..."
                            className="
                            w-full
                            rounded-2xl
                            border
                            border-white/10
                            bg-black/40
                            backdrop-blur-md
                            px-6
                            py-4
                            text-white
                            outline-none
                            focus:border-white/30
                            "
                        />

                        <button
                            disabled={!workArea.trim()}
                            onClick={() => {

                                if (workArea.trim()) {
                                    choose(workArea.trim());
                                }

                            }}
                            className="
                            rounded-full
                            px-8
                            py-3
                            bg-gradient-to-r
                            from-zinc-200
                            to-white
                            text-black
                            font-medium
                            transition-all
                            hover:scale-105
                            disabled:opacity-40
                            disabled:hover:scale-100
                            "
                        >
                            Continue
                        </button>

                    </div>

                ) : (

                    <div className="flex flex-wrap gap-4">

                        {question.options.map((option) => (

                            <button
                                key={option}
                                onClick={() => choose(option)}
                                className={`
                                rounded-full
                                px-6
                                py-3
                                backdrop-blur-md
                                transition-all
                                duration-200
                                active:scale-95
                                ${selectedPriorities.includes(option)
                                        ? "bg-emerald-500 text-black"
                                        : "bg-black/30 text-white hover:bg-white/10"
                                    }
                                `}
                            >
                                {option}
                            </button>

                        ))}

                    </div>

                )}

                {question.key === "priority" && (
                    <p className="mt-6 text-sm text-white/50">
                        Select any two options.
                    </p>
                )}

            </div>

        </div>
    );
}
