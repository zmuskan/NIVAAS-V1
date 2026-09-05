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

/**
 * Builds a short, natural-language explanation of why a locality was
 * recommended, entirely from backend-provided signals. No locality names
 * or static copy are hardcoded — everything is derived from the match data.
 */
function generateNarrative(match: Match): string {
    const { locality } = match;

    // Scores may or may not be present depending on the backend response.
    // Treat them defensively — they can arrive as 0-1 or 0-100 scales.
    const normalize = (score?: number) => {
        if (score === undefined || score === null || Number.isNaN(score)) {
            return undefined;
        }
        return score > 1 ? score / 100 : score;
    };

    const overall = normalize(locality.overallScore);
    const inventory = normalize(locality.inventoryScore);
    const density = normalize(locality.densityScore);

    const tier = (score?: number) => {
        if (score === undefined) return undefined;
        if (score >= 0.75) return "high" as const;
        if (score >= 0.45) return "moderate" as const;
        return "low" as const;
    };

    const overallTier = tier(overall);
    const inventoryTier = tier(inventory);
    const densityTier = tier(density);

    const clauses: string[] = [];

    // Overall fit framing.
    if (overallTier === "high") {
        clauses.push("this locality lines up closely with what you're looking for");
    } else if (overallTier === "moderate") {
        clauses.push("this locality covers most of what you're looking for");
    } else if (overallTier === "low") {
        clauses.push("this locality touches on some of your priorities");
    } else {
        clauses.push("this locality was shortlisted based on your preferences");
    }

    // Rent context.
    if (locality.avgRent !== undefined) {
        clauses.push(
            `average rents are around ${inr(locality.avgRent)} per month`
        );
    }

    // Inventory / choice.
    if (locality.listingCount !== undefined) {
        const listingsPhrase =
            inventoryTier === "high"
                ? "giving you plenty of rental choice"
                : inventoryTier === "moderate"
                    ? "giving you a healthy amount of rental choice"
                    : "with active rental inventory currently available";
        clauses.push(listingsPhrase);
    }

    // Density / feel of the neighbourhood.
    if (densityTier === "high") {
        clauses.push("in a busier, well-connected pocket of the city");
    } else if (densityTier === "low") {
        clauses.push("in a quieter, more spread-out part of the city");
    } else if (densityTier === "moderate") {
        clauses.push("in a balanced, moderately dense part of the city");
    }

    // Stitch clauses into a flowing sentence.
    const [first, ...rest] = clauses;

    if (!first) {
        return "Recommended based on your preferences.";
    }

    if (rest.length === 0) {
        return `${first.charAt(0).toUpperCase()}${first.slice(1)}.`;
    }

    const sentence = `${first}, ${rest.join(", ")}.`;
    return `${sentence.charAt(0).toUpperCase()}${sentence.slice(1)}`;
}

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

    const topMatches = matches.slice(0, 3);
    const remainingMatches = matches.slice(3);

    const goToLocality = (name: string) =>
        navigate(`/locality/${encodeURIComponent(name)}`);

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
                    {topMatches.map((m, i) => (
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
                                        {generateNarrative(m)}
                                    </p>

                                    <div className="mt-7 grid gap-5 sm:grid-cols-3">
                                        <Fact
                                            label="Homes listed"
                                            value={m.locality.listingCount?.toLocaleString("en-IN") ?? "N/A"}
                                        />

                                        <Fact
                                            label="Inventory Score"
                                            value={
                                                m.locality.inventoryScore !== undefined
                                                    ? `${Math.round(
                                                        (m.locality.inventoryScore <= 1
                                                            ? m.locality.inventoryScore * 100
                                                            : m.locality.inventoryScore),
                                                    )}`
                                                    : "N/A"
                                            }
                                        />

                                        <Fact
                                            label="Rent range"
                                            value={m.locality.minRent !== undefined && m.locality.maxRent !== undefined
                                                ? `${inr(m.locality.minRent)} - ${inr(m.locality.maxRent)}`
                                                : "N/A"}
                                        />
                                    </div>

                                    <div className="mt-7">
                                        <span className="inline-flex rounded-full bg-accent/15 px-3 py-1.5 text-[0.55rem] track-wide text-accent">
                                            Match Score {m.locality.overallScore !== undefined
                                                ? `${Math.round(
                                                    (m.locality.overallScore <= 1
                                                        ? m.locality.overallScore * 100
                                                        : m.locality.overallScore),
                                                )}%`
                                                : "N/A"}
                                        </span>

                                        <p className="mt-3 track-wide text-[0.5rem] text-accent">
                                            Why NIVAAS picked this
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

                                        <div className="mt-3 flex flex-wrap gap-2">
                                            {m.locality.highlights?.map((h) => (
                                                <span
                                                    key={h}
                                                    className="rounded-full bg-primary/10 px-3 py-1 text-xs"
                                                >
                                                    {h}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => goToLocality(m.locality.name)}
                                        className="mt-8 rounded-full bg-[image:var(--gradient-dusk)] px-9 py-3.5 text-xs track-wide text-primary-foreground transition-transform hover:-translate-y-0.5"
                                    >
                                        Explore {m.locality.name}
                                    </button>
                                </div>
                            </div>
                        </motion.article>
                    ))}
                </div>

                <div className="my-20 border-t border-white/10" />

                {remainingMatches.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.9, ease, delay: 0.2 }}
                        className="mt-20 opacity-85"
                    >
                        <p className="track-wide text-[0.55rem] text-accent">
                            More neighbourhoods worth exploring
                        </p>

                        <p className="mt-3 max-w-xl text-sm font-light text-muted-foreground">
                            These neighbourhoods didn't make the top three, but
                            may still suit your preferences.
                        </p>

                        <div className="mt-7 -mx-5 flex snap-x snap-mandatory gap-4 overflow-x-auto px-5 pb-4">
                            {remainingMatches.map((m, i) => (
                                <div
                                    key={m.locality.id}
                                    className="w-[320px] shrink-0 snap-start overflow-hidden rounded-2xl bg-black/60 backdrop-blur-md"
                                >
                                    <div className="relative h-32">
                                        <img
                                            src={covers[(i + 3) % covers.length]}
                                            alt={`${m.locality.name} rentals`}
                                            className="h-full w-full object-cover"
                                        />
                                        <div className="veil absolute inset-0 opacity-70" />
                                    </div>

                                    <div className="p-5">
                                        <h4 className="text-lg text-foreground">
                                            {m.locality.name}
                                        </h4>

                                        <div className="mt-3 flex items-center justify-between gap-3">
                                            <div>
                                                <p className="track-wide text-[0.45rem] text-muted-foreground">
                                                    Avg rent
                                                </p>
                                                <p className="mt-0.5 text-sm text-foreground">
                                                    {m.locality.avgRent !== undefined
                                                        ? inr(m.locality.avgRent)
                                                        : "N/A"}
                                                    <span className="text-[0.65rem] text-muted-foreground">
                                                        {" "}/mo
                                                    </span>
                                                </p>
                                            </div>

                                            <div className="text-right">
                                                <p className="track-wide text-[0.45rem] text-muted-foreground">
                                                    Listed homes
                                                </p>
                                                <p className="mt-0.5 text-sm text-foreground">
                                                    {m.locality.listingCount?.toLocaleString("en-IN") ?? "N/A"}
                                                </p>
                                            </div>
                                        </div>

                                        <button
                                            onClick={() => goToLocality(m.locality.name)}
                                            className="mt-5 w-full rounded-full border border-white/15 px-4 py-2 text-[0.65rem] track-wide text-foreground transition-colors hover:border-white/30 hover:bg-white/5"
                                        >
                                            Explore {m.locality.name}
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                )}

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
