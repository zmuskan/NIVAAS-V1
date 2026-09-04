import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

import {
    inr,
    matchLabels,
    type Answers,
    type Match,
} from "../../data/nivaas";

import towers from "@/assets/tower.png";
import street from "@/assets/street.png";
import courtyard from "@/assets/courtyard.png";

const covers = [towers, street, courtyard];
const ease = [0.22, 1, 0.36, 1] as const;

export function Results({
    answers,
    matches,
    onRestart,
}: {
    answers: Answers;
    matches: Match[];
    onRestart: () => void;
}) {
    const navigate = useNavigate();

    return (
        <section className="relative min-h-screen px-5 pb-32 pt-24">
            <div className="pointer-events-none absolute inset-x-0 top-0 h-[70vh] bg-[radial-gradient(ellipse_at_50%_0%,color-mix(in_oklab,var(--violet-glow)_26%,transparent),transparent_70%)]" />

            <div className="relative mx-auto max-w-6xl">
                <motion.div
                    initial={{ opacity: 0, y: 24 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, ease }}
                    className="max-w-2xl"
                >
                    <p className="track-wide text-[0.55rem] text-accent">
                        {answers.name
                            ? `${answers.name}, here's your Bangalore`
                            : "Here's your Bangalore"}
                    </p>

                    <h2 className="mt-6 text-4xl leading-[1.05] text-foreground sm:text-6xl">
                        Three neighbourhoods where
                        <span className="text-dusk-gradient">
                            {" "}your home already exists
                        </span>
                    </h2>

                    <p className="mt-6 text-sm font-light text-muted-foreground sm:text-base">
                        Ranked on what you told us — your budget, your{" "}
                        {answers.workArea ?? "work area"} run, your priorities
                        and who's moving in.
                    </p>
                </motion.div>

                <div className="mt-16 space-y-8">
                    {matches.map((m, i) => (
                        <motion.article
                            key={m.locality.id}
                            initial={{ opacity: 0, y: 50 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{
                                duration: 0.9,
                                delay: i * 0.14,
                                ease,
                            }}
                            className="bg-black/60 backdrop-blur-md overflow-hidden rounded-3xl"
                        >
                            <div className="grid md:grid-cols-5">
                                <div className="relative h-56 md:col-span-2 md:h-full">
                                    <img
                                        src={covers[i % covers.length]}
                                        alt={`${m.locality.name} rentals`}
                                        className="h-full w-full object-cover"
                                    />

                                    <div className="veil absolute inset-0 opacity-70" />

                                    <span className="rounded-full bg-zinc-900/80 backdrop-blur-md absolute left-5 top-5 px-4 py-2 track-wide text-[0.5rem] text-foreground">
                                        {matchLabels[i]}
                                    </span>
                                </div>

                                <div className="p-7 sm:p-9 md:col-span-3">
                                    <div className="flex flex-wrap items-baseline justify-between gap-3">
                                        <div>
                                            <h3 className="text-3xl text-foreground sm:text-4xl">
                                                {m.locality.name}
                                            </h3>

                                            <p className="mt-1.5 text-xs text-accent">
                                                Locality profile
                                            </p>
                                        </div>

                                        <div className="text-right">
                                            <p className="track-wide text-[0.5rem] text-muted-foreground">
                                                Average rent
                                            </p>

                                            <p className="mt-1 text-2xl font-light text-foreground">
                                                {m.locality.avgRent !== undefined
                                                    ? inr(m.locality.avgRent)
                                                    : "N/A"}
                                                <span className="text-xs text-muted-foreground">
                                                    {" "} /mo
                                                </span>
                                            </p>
                                        </div>
                                    </div>

                                    <p className="mt-5 text-sm font-light leading-relaxed text-muted-foreground">
                                        {m.reasons[0] ?? "Recommendation data available."}
                                    </p>

                                    <div className="mt-7 grid gap-5 sm:grid-cols-3">
                                        <Fact
                                            label="Homes listed"
                                            value={m.locality.listingCount?.toLocaleString("en-IN") ?? "N/A"}
                                        />

                                        <Fact
                                            label="Availability"
                                            value="Backend data"
                                        />

                                        <Fact
                                            label="Rent range"
                                            value={m.locality.minRent !== undefined && m.locality.maxRent !== undefined
                                                ? `${inr(m.locality.minRent)} - ${inr(m.locality.maxRent)}`
                                                : "N/A"}
                                        />
                                    </div>

                                    <div className="mt-7">
                                        <p className="track-wide text-[0.5rem] text-accent">
                                            Why this fits you
                                        </p>

                                        <ul className="mt-4 space-y-2">
                                            {m.reasons.map((r) => (
                                                <li
                                                    key={r}
                                                    className="flex gap-3 text-sm font-light text-muted-foreground"
                                                >
                                                    <span className="mt-2 size-1 shrink-0 rounded-full bg-accent" />
                                                    {r}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    <button
                                        onClick={() =>
                                            navigate(
                                                `/locality/${encodeURIComponent(
                                                    m.locality.name
                                                )}`
                                            )
                                        }
                                        className="mt-8 rounded-full bg-[image:var(--gradient-dusk)] px-9 py-3.5 text-xs track-wide text-primary-foreground transition-transform hover:-translate-y-0.5"
                                    >
                                        Explore {m.locality.name}
                                    </button>
                                </div>
                            </div>
                        </motion.article>
                    ))}
                </div>

                <div className="mt-16 text-center">
                    <button
                        onClick={onRestart}
                        className="track-wide text-[0.55rem] text-muted-foreground transition-colors hover:text-foreground"
                    >
                        Start the journey again
                    </button>
                </div>
            </div>
        </section>
    );
}

function Fact({
    label,
    value,
}: {
    label: string;
    value: string;
}) {
    return (
        <div>
            <p className="track-wide text-[0.5rem] text-muted-foreground">
                {label}
            </p>

            <p className="mt-2 text-base text-foreground">
                {value}
            </p>
        </div>
    );
}
