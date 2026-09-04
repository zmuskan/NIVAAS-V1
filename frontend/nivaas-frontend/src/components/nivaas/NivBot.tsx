import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { inr, type Locality, type Match } from "../../data/nivaas";

type Msg = { role: "bot" | "user"; text: string };

function find(text: string, matches: Match[]): Locality[] {
    const t = text.toLowerCase();
    return matches
        .map((match) => match.locality)
        .filter(
            (l) => t.includes(l.name.toLowerCase()) || t.includes(l.id.replace("-", " ")),
        );
}

function compare(a: Locality, b: Locality) {
    return [
        `${a.name}: ${a.avgRent !== undefined ? inr(a.avgRent) : "rent unavailable"}.`,
        `${b.name}: ${b.avgRent !== undefined ? inr(b.avgRent) : "rent unavailable"}.`,
    ].join(" ");
}

function answer(text: string, matches: Match[]): string {
    const t = text.toLowerCase();
    const hits = find(text, matches);

    if (hits.length >= 2 && hits[0] && hits[1]) return compare(hits[0], hits[1]);

    if (hits.length === 1 && hits[0]) {
        const l = hits[0];
        return `${l.name}: backend locality data is available for this recommendation.`;
    }

    if (matches.length && /my|match|best|shortlist|recommend/.test(t)) {
        return `Your shortlist: ${matches
            .map((m) => `${m.locality.name} (${m.locality.avgRent !== undefined ? inr(m.locality.avgRent) : "rent unavailable"})`)
            .join(", ")}. Ask me to compare any two.`;
    }

    return "I can compare two areas, or answer on rents, availability, furnishing and BHK mix. Try “compare HSR Layout and Whitefield” or “furnished homes in Indiranagar”.";
}

export function NivBot({ matches }: { matches: Match[] }) {
    console.log("NIVBOT RENDERED");
    const [open, setOpen] = useState(false);
    const [input, setInput] = useState("");
    const [msgs, setMsgs] = useState<Msg[]>([
        {
            role: "bot",
            text: "I'm NivBot. Ask me to compare neighbourhoods or dig into what's actually available to rent.",
        },
    ]);
    const endRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        endRef.current?.scrollIntoView({ block: "nearest" });
    }, [msgs, open]);

    const send = (text: string) => {
        if (!text.trim()) return;
        setInput("");
        setMsgs((m) => [...m, { role: "user", text }]);
        setTimeout(
            () => setMsgs((m) => [...m, { role: "bot", text: answer(text, matches) }]),
            420,
        );
    };

    const suggestions = matches.length
        ? [
            `Compare ${matches[0]?.locality.name} and ${matches[1]?.locality.name}`,
            `Furnished homes in ${matches[0]?.locality.name}`,
            "Which area is most affordable?",
        ]
        : ["Which area has the most options?", "Which area is most affordable?"];

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
                                <p className="mt-1 text-sm text-foreground">Rental questions, answered</p>
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
                                    className={`max-w-[88%] rounded-2xl px-4 py-3 text-xs leading-relaxed ${m.role === "bot"
                                        ? "glass-soft text-muted-foreground"
                                        : "ml-auto bg-primary/30 text-foreground"
                                        }`}
                                >
                                    {m.text}
                                </div>
                            ))}
                            <div ref={endRef} />
                        </div>

                        <div className="mt-3 flex flex-wrap gap-2">
                            {suggestions.map((s) => (
                                <button
                                    key={s}
                                    onClick={() => send(s)}
                                    className="glass-soft rounded-full px-3 py-1.5 text-[0.6rem] text-muted-foreground transition-colors hover:text-foreground"
                                >
                                    {s}
                                </button>
                            ))}
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
