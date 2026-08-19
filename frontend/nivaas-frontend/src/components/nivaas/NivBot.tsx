import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { inr, localities, type Locality, type Match } from "@/data/nivaas";

type Msg = { role: "bot" | "user"; text: string };

function find(text: string): Locality[] {
    const t = text.toLowerCase();
    return localities.filter(
        (l) => t.includes(l.name.toLowerCase()) || t.includes(l.id.replace("-", " ")),
    );
}

function share(_l: Locality, list: { label: string; share: number }[], word: string) {
    const hit = list.find((d) => d.label.toLowerCase().includes(word));
    return hit ? `${hit.share}% of listings` : null;
}

function compare(a: Locality, b: Locality) {
    const cheaper = a.avgRent <= b.avgRent ? a : b;
    const deeper = a.listings >= b.listings ? a : b;
    return [
        `${a.name}: ${inr(a.avgRent)} average, ${a.listings.toLocaleString("en-IN")} homes listed, mostly ${a.propertyTypes[0]?.label.toLowerCase()}.`,
        `${b.name}: ${inr(b.avgRent)} average, ${b.listings.toLocaleString("en-IN")} homes listed, mostly ${b.propertyTypes[0]?.label.toLowerCase()}.`,
        `${cheaper.name} is the lighter rent; ${deeper.name} gives you more to choose from.`,
    ].join(" ");
}

function answer(text: string, matches: Match[]): string {
    const t = text.toLowerCase();
    const hits = find(text);

    if (hits.length >= 2 && hits[0] && hits[1]) return compare(hits[0], hits[1]);

    if (/cheap|afford|lowest|budget/.test(t)) {
        const l = [...localities].sort((a, b) => a.avgRent - b.avgRent)[0]!;
        return `${l.name} has the lowest average rent of the areas I track — ${inr(l.avgRent)} a month, with homes from ${l.rentRange.split("–")[0]?.trim()}.`;
    }

    if (/most|choice|options|inventory|available|availability/.test(t)) {
        const l = [...localities].sort((a, b) => b.listings - a.listings)[0]!;
        return `${l.name} has the deepest inventory right now — ${l.listings.toLocaleString("en-IN")} active rentals and ${l.availability.toLowerCase()} availability.`;
    }

    if (hits.length === 1 && hits[0]) {
        const l = hits[0];
        if (/furnish/.test(t)) {
            return `In ${l.name}, ${l.furnishing.map((f) => `${f.label.toLowerCase()} ${f.share}%`).join(", ")}. ${share(l, l.furnishing, "fully") ?? ""} come move-in ready.`;
        }
        if (/3 ?bhk|three/.test(t)) {
            return `3 BHK homes are ${l.bhkMix.find((b) => b.label === "3 BHK")?.share ?? 0}% of ${l.name} listings — roughly ${Math.round((l.listings * (l.bhkMix.find((b) => b.label === "3 BHK")?.share ?? 0)) / 100).toLocaleString("en-IN")} homes.`;
        }
        if (/1 ?bhk|studio|single/.test(t)) {
            return `1 BHK homes are ${l.bhkMix.find((b) => b.label === "1 BHK")?.share ?? 0}% of ${l.name} listings, and rents start around ${l.rentRange.split("–")[0]?.trim()}.`;
        }
        if (/rent|price|cost/.test(t)) {
            return `${l.name} averages ${inr(l.avgRent)} a month, with the listed range at ${l.rentRange}.`;
        }
        return `${l.name} — ${l.blurb} Average rent ${inr(l.avgRent)}, ${l.listings.toLocaleString("en-IN")} homes listed, ${l.availability.toLowerCase()} availability.`;
    }

    if (matches.length && /my|match|best|shortlist|recommend/.test(t)) {
        return `Your shortlist: ${matches
            .map((m) => `${m.locality.name} (${inr(m.locality.avgRent)}, ${m.locality.listings.toLocaleString("en-IN")} homes)`)
            .join(", ")}. Ask me to compare any two.`;
    }

    return "I can compare two areas, or answer on rents, availability, furnishing and BHK mix. Try “compare HSR Layout and Whitefield” or “furnished homes in Indiranagar”.";
}

export function NivBot({ matches }: { matches: Match[] }) {
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
