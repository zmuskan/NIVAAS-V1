import { useEffect, useRef, useState, type ChangeEvent } from "react";
import { AnimatePresence, motion, useScroll, useTransform } from "framer-motion";
import metro from "@/assets/metro.png";
import towers from "@/assets/tower.png";
import street from "@/assets/street.png";
import courtyard from "@/assets/courtyard.png";
import { getLocalities } from "@/api/localities";
import {
    budgetOptions,
    lifestyleOptions,
    priorityOptions,
    type Answers,
    type BudgetKey,
    type LifestyleKey,
    type PriorityKey,
} from "@/data/nivaas";

const ease = [0.22, 1, 0.36, 1] as const;
const backgrounds = [metro, towers, courtyard, street, towers];

function Chapter({
    id,
    image,
    children,
    align = "center",
}: {
    id: string;
    image: string;
    children: React.ReactNode;
    align?: "center" | "end";
}) {
    const ref = useRef<HTMLElement>(null);
    const { scrollYProgress } = useScroll({
        target: ref,
        offset: ["start end", "end start"],
    });
    const y = useTransform(scrollYProgress, [0, 1], ["-8%", "8%"]);
    const scale = useTransform(scrollYProgress, [0, 0.5, 1], [1.14, 1.04, 1.14]);
    const contentY = useTransform(scrollYProgress, [0, 1], ["6%", "-6%"]);
    const opacity = useTransform(scrollYProgress, [0, 0.18, 0.82, 1], [0, 1, 1, 0]);

    return (
        <section
            id={id}
            ref={ref}
            className="relative flex min-h-screen w-full items-center overflow-hidden"
        >
            <motion.div style={{ y, scale }} className="absolute inset-[-10%]">
                <img src={image} alt="" className="h-full w-full object-cover" />
            </motion.div>
            <div className="veil absolute inset-0" />
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_110%,color-mix(in_oklab,var(--ember)_26%,transparent),transparent_65%)]" />
            <motion.div
                style={{ y: contentY, opacity }}
                className={`relative z-10 mx-auto w-full max-w-3xl px-6 py-28 ${align === "end" ? "self-end pb-24" : ""
                    }`}
            >
                {children}
            </motion.div>
        </section>
    );
}

function Prompt({
    step,
    eyebrow,
    title,
    caption,
}: {
    step: string;
    eyebrow: string;
    title: string;
    caption?: string;
}) {
    return (
        <div>
            <div className="flex items-center gap-4">
                <span className="track-wide text-[0.55rem] text-accent">{step}</span>
                <span className="h-px w-14 bg-accent/50" />
                <span className="track-wide text-[0.55rem] text-muted-foreground">{eyebrow}</span>
            </div>
            <h2 className="mt-6 text-4xl leading-[1.05] text-foreground sm:text-6xl">{title}</h2>
            {caption && (
                <p className="mt-5 max-w-xl text-sm font-light text-muted-foreground sm:text-base">
                    {caption}
                </p>
            )}
        </div>
    );
}

function Chip({
    active,
    onClick,
    children,
}: {
    active?: boolean;
    onClick: () => void;
    children: React.ReactNode;
}) {
    return (
        <button
            onClick={onClick}
            className={`rounded-full bg-black/40 hover:bg-black/60 border border-white/20 backdrop-blur-sm px-6 py-3.5 text-sm transition-all duration-500 hover:-translate-y-0.5 ${active
                ? "bg-primary/35 text-foreground ring-1 ring-primary"
                : "text-muted-foreground"
                }`}
        >
            {children}
        </button>
    );
}

export function Journey({ onComplete }: { onComplete: (answers: Answers) => void }) {
    const [answers, setAnswers] = useState<Answers>({ name: "", priorities: [] });
    const [nameDraft, setNameDraft] = useState("");
    const [query, setQuery] = useState("");
    const [workAreas, setWorkAreas] = useState<
        { locality: string }[]
    >([]);
    const [step, setStep] = useState(0); // chapters unlocked
    const [pause, setPause] = useState<"hidden" | "showing">("hidden");

    const unlock = (n: number, id: string) => {
        setStep((s) => Math.max(s, n));
        requestAnimationFrame(() => {
            setTimeout(() => {
                document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 220);
        });
    };

    const togglePriority = (key: PriorityKey) => {
        setAnswers((a) => {
            const has = a.priorities.includes(key);
            const next = has
                ? a.priorities.filter((p) => p !== key)
                : [...a.priorities, key].slice(0, 3);
            return { ...a, priorities: next };
        });
    };

    const setLifestyle = (key: LifestyleKey) => {
        setAnswers((a) => ({ ...a, lifestyle: key }));
        unlock(5, "ch-pause");
        setTimeout(() => setPause("showing"), 700);
    };

    useEffect(() => {
        getLocalities().then((data) => {
            setWorkAreas(data);
        });
    }, []);

    useEffect(() => {
        if (pause !== "showing") return;
        const t = setTimeout(() => onComplete(answers), 4200);
        return () => clearTimeout(t);
    }, [pause, answers, onComplete]);

    const matches = query.trim()
        ? workAreas
            .filter((w) =>
                w.locality
                    .toLowerCase()
                    .includes(
                        query.trim().toLowerCase()
                    )
            )
            .slice(0, 10)
        : workAreas.slice(0, 10);

    return (
        <div className="relative">
            {/* Intro + name (image background + immediate question) */}
            <section className="relative h-screen w-full overflow-hidden">
                <img
                    src={backgrounds[Math.min(step, backgrounds.length - 1)]}
                    alt="background"
                    className="absolute inset-0 h-full w-full object-cover"
                />
                <div className="absolute inset-0 bg-black/60" />

                <div className="relative z-10 flex h-full flex-col items-center justify-center px-6 text-center">
                    <div className="max-w-4xl mx-auto bg-black/30 backdrop-blur-md border border-white/10 rounded-3xl p-10">
                        <motion.form
                            initial={{ opacity: 0, y: 8 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.8 }}
                            onSubmit={(e) => {
                                e.preventDefault();
                                if (!nameDraft.trim()) return;
                                setAnswers((a) => ({ ...a, name: nameDraft.trim() }));
                                unlock(1, "ch-budget");
                            }}
                            className="w-full max-w-md text-left"
                        >
                            <h2 className="text-2xl font-light text-foreground">What should we call you?</h2>
                            <input
                                id="nivaas-name"
                                value={nameDraft}
                                onChange={(e: ChangeEvent<HTMLInputElement>) => setNameDraft(e.target.value)}
                                placeholder="Your name"
                                autoComplete="given-name"
                                className="mt-6 w-full rounded-2xl border border-input bg-transparent px-5 py-4 text-base text-foreground outline-none transition-colors placeholder:text-muted-foreground/70 focus:border-primary"
                            />
                            <button
                                type="submit"
                                disabled={!nameDraft.trim()}
                                className="mt-5 w-full rounded-full bg-[image:var(--gradient-dusk)] px-8 py-4 text-xs track-wide text-primary-foreground transition-opacity disabled:opacity-30"
                            >
                                Continue
                            </button>
                        </motion.form>
                    </div>
                </div>
            </section>

            {step >= 1 && (
                <Chapter id="ch-budget" image={towers}>
                    <Prompt
                        step="01"
                        eyebrow={answers.name ? `Hello, ${answers.name}` : "Budget"}
                        title="What feels comfortable each month?"
                        caption="Rent is a feeling before it is a number. Pick the range you'd sign without hesitating."
                    />
                    <div className="mt-10 flex flex-wrap gap-3">
                        {budgetOptions.map((b) => (
                            <Chip
                                key={b.key}
                                active={answers.budget === b.key}
                                onClick={() => {
                                    setAnswers((a) => ({ ...a, budget: b.key as BudgetKey }));
                                    unlock(2, "ch-work");
                                }}
                            >
                                {b.label}
                            </Chip>
                        ))}
                    </div>
                </Chapter>
            )}

            {step >= 2 && (
                <Chapter id="ch-work" image={metro}>
                    <Prompt
                        step="02"
                        eyebrow="Work or study"
                        title="Where does your day begin?"
                        caption="Start typing — we'll measure the city in minutes from there."
                    />
                    <div className="bg-black/60 backdrop-blur-md mt-10 rounded-3xl p-6">
                        <input
                            value={answers.workArea ?? query}
                            onChange={(e: ChangeEvent<HTMLInputElement>) => {
                                const value = e.target.value;

                                setQuery(value);

                                setAnswers((a) => ({
                                    ...a,
                                    workArea: value,
                                }));
                            }}
                            onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                    unlock(3, "ch-priorities");
                                }
                            }}
                            placeholder="Search an office, campus or area"
                            className="w-full rounded-2xl border border-input bg-transparent px-5 py-4 text-base text-foreground outline-none transition-colors placeholder:text-muted-foreground/70 focus:border-primary"
                        />
                        <div className="mt-4 space-y-2">
                            <AnimatePresence initial={false}>
                                {matches.map((w) => (
                                    <motion.button
                                        key={w.locality}
                                        layout
                                        initial={{ opacity: 0, y: 6 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0 }}
                                        onClick={() => {
                                            setAnswers((a) => ({ ...a, workArea: w.locality }));
                                            setQuery(w.locality);
                                            unlock(3, "ch-priorities");
                                        }}
                                        className={`block w-full rounded-2xl px-5 py-3.5 text-left text-sm transition-colors ${answers.workArea === w.locality
                                            ? "bg-primary/30 text-foreground"
                                            : "text-muted-foreground hover:bg-primary/15"
                                            }`}
                                    >
                                        {w.locality}
                                    </motion.button>
                                ))}
                            </AnimatePresence>
                            {matches.length === 0 && (
                                <p className="px-5 py-3 text-sm text-muted-foreground">
                                    No area by that name — try a nearby landmark.
                                </p>
                            )}
                        </div>
                    </div>
                </Chapter>
            )}

            {step >= 3 && (
                <Chapter id="ch-priorities" image={courtyard}>
                    <Prompt
                        step="03"
                        eyebrow="Priorities"
                        title="What matters most in a home?"
                        caption= "Choose up to two. We'll personalize recommendations around your priorities."
                    />
                    <div className="mt-10 flex flex-wrap gap-3">
                        {priorityOptions.map((p) => (
                            <Chip
                                key={p.key}
                                active={answers.priorities.includes(p.key)}
                                onClick={() => togglePriority(p.key)}
                            >
                                {p.label}
                            </Chip>
                        ))}
                    </div>
                    <button
                        disabled={answers.priorities.length === 0}
                        onClick={() => unlock(4, "ch-lifestyle")}
                        className="mt-10 rounded-full bg-[image:var(--gradient-dusk)] px-10 py-4 text-xs track-wide text-primary-foreground transition-opacity disabled:opacity-30"
                    >
                        {answers.priorities.length ? "Continue" : "Pick at least one"}
                    </button>
                </Chapter>
            )}

            {step >= 4 && (
                <Chapter id="ch-lifestyle" image={street}>
                    <Prompt
                        step="04"
                        eyebrow="Lifestyle"
                        title="Who's moving in?"
                        caption="The last question is the shortest one."
                    />
                    <div className="mt-10 flex flex-wrap gap-3">
                        {lifestyleOptions.map((l) => (
                            <Chip
                                key={l.key}
                                active={answers.lifestyle === l.key}
                                onClick={() => setLifestyle(l.key)}
                            >
                                {l.label}
                            </Chip>
                        ))}
                    </div>
                </Chapter>
            )}

            {step >= 5 && (
                <section
                    id="ch-pause"
                    className="relative flex h-screen w-full items-center justify-center overflow-hidden"
                >
                    <motion.img
                        initial={{ scale: 1.18, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 3.4, ease }}
                        src={courtyard}
                        alt="A residential Bangalore neighbourhood at dusk"
                        className="absolute inset-0 h-full w-full object-cover"
                    />
                    <div className="veil absolute inset-0" />
                    <div className="relative z-10 px-6 text-center">
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 1.6, delay: 0.6 }}
                            className="text-4xl font-light leading-tight text-foreground sm:text-6xl"
                        >
                            We've seen enough.
                        </motion.p>
                        <motion.p
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 1.6, delay: 2 }}
                            className="mt-7 track-wide text-[0.6rem] text-accent"
                        >
                            {answers.name
                                ? `Finding your Bangalore, ${answers.name}`
                                : "Finding your Bangalore"}
                        </motion.p>
                    </div>
                </section>
            )}
        </div>
    );
}
