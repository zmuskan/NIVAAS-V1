import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { askNivBot } from "../../api/nivbot";
import type { Match } from "../../data/nivaas";

type Msg = { role: "bot" | "user"; text: string };
type NivBotMode = "locality" | "recommendation";

type NivBotProps = {
    matches: Match[];
    localityName?: string;
    /**
     * "locality"       -> renders on a single locality profile page, acts as
     *                     an area advisor for that one place.
     * "recommendation" -> renders on the recommendations/listing page,
     *                     leads with comparison and ranking explanations.
     */
    mode?: NivBotMode;
};

const GREETINGS: Record<NivBotMode, string> = {
    locality:
        "I'm NivBot, your advisor for this area. Ask me about rent, affordability, what it feels like day-to-day, or the pros and cons of living here.",
    recommendation:
        "I'm NivBot. I can explain why a locality ranked where it did, break down trade-offs, or compare two areas side by side.",
};

const LOCALITY_CATEGORIES: Record<string, string[]> = {
    "Rent & Budget": [
        "What's the average rent here?",
        "Is this area affordable for me?",
        "Is this area expensive?",
    ],
    "Availability": [
        "How many listings are available?",
        "Is it easy to find a place here?",
    ],
    "Neighborhood Feel": [
        "Is this area crowded?",
        "Is it quiet here?",
    ],
    "Should I Move Here": [
        "Pros and cons of this area",
        "Is this locality worth considering?",
        "Any practical tips before I move here?",
    ],
};

const RECOMMENDATION_CATEGORIES: Record<string, string[]> = {
    "Why This Ranking": [
        "Why is this locality ranked here?",
        "What made this locality rank higher?",
    ],
    "Trade-offs": [
        "What are the trade-offs of this locality?",
        "Pros and cons",
    ],
    "Compare": [
        "Compare the top two localities",
        "Which of these is cheaper?",
        "Which of these has better availability?",
    ],
    "Fit For You": [
        "Which is better for a tight budget?",
        "Which is calmer to live in?",
    ],
    "Best Choice": [
        "Which locality would you personally choose?",
        "Which offers the best balance overall?",
    ],
};

export function NivBot({ matches, localityName = "", mode = "locality" }: NivBotProps) {
    const [open, setOpen] = useState(false);
    const [input, setInput] = useState("");
    const [msgs, setMsgs] = useState<Msg[]>([{ role: "bot", text: GREETINGS[mode] }]);
    const endRef = useRef<HTMLDivElement>(null);

    // Reset the greeting if the page context (mode) changes, e.g. the same
    // component instance is reused across a locality page and a
    // recommendations page.
    useEffect(() => {
        setMsgs([{ role: "bot", text: GREETINGS[mode] }]);
    }, [mode]);

    useEffect(() => {
        endRef.current?.scrollIntoView({ block: "nearest" });
    }, [msgs, open]);

    // On the recommendations page, "compare" style questions should carry
    // the top matches along so the backend can look up all of them, not
    // just the single locality currently in view.
    const compareLocalities =
        mode === "recommendation"
            ? matches.slice(0, 3).map((m) => m.locality.name)
            : [];

    const send = async (text: string) => {
        const gibberish = text.trim().length < 3 || /^[^a-zA-Z]+$/.test(text);

        if (gibberish) {
            setMsgs((m) => [
                ...m,
                {
                    role: "bot",
                    text: "I couldn't understand that question. Try asking about rent, availability, the neighborhood feel, pros and cons, or affordability.",
                },
            ]);
            return;
        }

        setInput("");
        setMsgs((m) => [...m, { role: "user", text }]);

        try {
            const response = await askNivBot(text, localityName, { mode, compareLocalities });

            setMsgs((m) => [...m, { role: "bot", text: response.answer }]);
        } catch {
            setMsgs((m) => [
                ...m,
                { role: "bot", text: "Sorry, I couldn't generate a response. Please try again." },
            ]);
        }
    };

    const categories = mode === "recommendation" ? RECOMMENDATION_CATEGORIES : LOCALITY_CATEGORIES;
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

    useEffect(() => {
        setSelectedCategory(null);
    }, [mode]);

    return (
        <>
            <AnimatePresence>
                {open && (
                    <motion.div
                        initial={{ opacity: 0, y: 24, scale: 0.96 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 24, scale: 0.96 }}
                        transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                        className="bg-black/80 backdrop-blur-md border border-white/10 fixed bottom-24 right-5 z-50 flex h-[26rem] w-[min(22rem,calc(100vw-2.5rem))] flex-col rounded-3xl p-5"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="track-wide text-[0.5rem] text-accent">NivBot</p>
                                <p className="mt-1 text-sm text-foreground">
                                    {mode === "recommendation" ? "Compare & decide" : "Rental questions, answered"}
                                </p>
                            </div>
                            <button
                                onClick={() => setOpen(false)}
                                aria-label="Close NivBot"
                                className="text-muted-foreground transition-colors hover:text-foreground"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="mt-5 flex-1 space-y-3 overflow-y-auto pr-1">
                            {msgs.map((m, i) => (
                                <div
                                    key={i}
                                    className={`max-w-[88%] whitespace-pre-line rounded-2xl px-4 py-3 text-xs leading-relaxed ${m.role === "bot"
                                        ? "glass-soft text-muted-foreground"
                                        : "ml-auto bg-primary/30 text-foreground"
                                        }`}
                                >
                                    {m.text}
                                </div>
                            ))}
                            <div ref={endRef} />
                        </div>

                        <div className="mt-3">
                            {!selectedCategory ? (
                                <div className="flex flex-wrap gap-2">
                                    {Object.keys(categories).map((category) => (
                                        <button
                                            key={category}
                                            onClick={() => setSelectedCategory(category)}
                                            className="glass-soft rounded-full px-3 py-1.5 text-[0.6rem]"
                                        >
                                            {category}
                                        </button>
                                    ))}
                                </div>
                            ) : (
                                <div className="flex flex-wrap gap-2">
                                    {categories[selectedCategory]?.map((question) => (
                                        <button
                                            key={question}
                                            onClick={() => send(question)}
                                            className="glass-soft rounded-full px-3 py-1.5 text-[0.6rem]"
                                        >
                                            {question}
                                        </button>
                                    ))}

                                    <button
                                        onClick={() => setSelectedCategory(null)}
                                        className="glass-soft rounded-full px-3 py-1.5 text-[0.6rem]"
                                    >
                                        ← Back
                                    </button>
                                </div>
                            )}
                        </div>

                        <form
                            onSubmit={(e) => {
                                e.preventDefault();
                                send(input);
                            }}
                            className="mt-3 flex gap-2"
                        >
                            <input
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask NivBot…"
                                className="flex-1 rounded-full border border-input bg-transparent px-4 py-3 text-xs text-foreground outline-none focus:border-primary"
                            />
                            <button
                                type="submit"
                                className="rounded-full bg-[image:var(--gradient-dusk)] px-5 text-xs text-primary-foreground"
                            >
                                Ask
                            </button>
                        </form>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 }}
                whileHover={{ scale: 1.05 }}
                onClick={() => setOpen((o) => !o)}
                className="glass fixed bottom-6 right-5 z-50 flex items-center gap-3 rounded-full px-5 py-4 text-xs track-wide text-foreground shadow-[var(--shadow-glow)]"
            >
                <span className="size-2 rounded-full bg-accent" />
                NivBot
            </motion.button>
        </>
    );
}
