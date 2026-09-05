import { motion } from "framer-motion";
import { AreaMap } from "@/components/nivaas/AreaMap";
import { inr, type Locality } from "../../data/nivaas";
import towers from "@/assets/tower.png";
import street from "@/assets/street.png";
import courtyard from "@/assets/courtyard.png";
import metro from "@/assets/metro.png";

const ease = [0.22, 1, 0.36, 1] as const;
const heroImages = [street, courtyard, towers, metro];

function heroFor(id: string): string {
    const imageIndex = [...id].reduce(
        (total, character) => total + character.charCodeAt(0),
        0,
    ) % heroImages.length;
    return heroImages[imageIndex] ?? courtyard;
}

/* ------------------------------------------------------------------ */
/*  Score → language helpers                                          */
/*                                                                     */
/*  Everything below is derived purely from the numeric fields on a   */
/*  Locality (overallScore, inventoryScore, densityScore, avgRent,    */
/*  listingCount). Nothing here references a specific locality name,  */
/*  so the same logic produces sensible copy for every row in the     */
/*  database.                                                         */
/* ------------------------------------------------------------------ */

type Tier = "high" | "moderate" | "low";

function scorePercent(score?: number): number | undefined {
    if (score === undefined || score === null || Number.isNaN(score)) {
        return undefined;
    }
    return Math.max(0, Math.min(100, score <= 1 ? score * 100 : score));
}

function scoreTier(score?: number, highMin = 75, moderateMin = 45): Tier | undefined {
    const percent = scorePercent(score);
    if (percent === undefined) {
        return undefined;
    }
    if (percent >= highMin) return "high";
    if (percent >= moderateMin) return "moderate";
    return "low";
}

function getBestForTags(locality: Locality): string[] {
    const densityTier = scoreTier(locality.densityScore);
    const inventoryTier = scoreTier(locality.inventoryScore);

    if (densityTier === "high" && inventoryTier === "high") {
        return ["Working Professionals", "Flatmates", "Students"];
    }
    if (densityTier === "low") {
        return ["Families", "Long-Term Renters", "Working Professionals"];
    }
    return ["Working Professionals", "Families", "Flatmates"];
}

function Panel({
    children,
    className = "",
    delay = 0,
}: {
    children: React.ReactNode;
    className?: string;
    delay?: number;
}) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.9, delay, ease }}
            className={`bg-black/60 backdrop-blur-md rounded-3xl p-6 sm:p-8 ${className}`}
        >
            {children}
        </motion.div>
    );
}

export function LocalityProfile({
    locality,
    onBack,
}: {
    locality: Locality;
    onBack: () => void;
}) {
    const bestFor = getBestForTags(locality);

    return (
        <section className="min-h-screen pb-24">
            <div className="relative h-[60vh] overflow-hidden">
                <motion.img
                    initial={{ scale: 1.14, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 2, ease }}
                    src={heroFor(locality.id)}
                    alt={`${locality.name} at dusk`}
                    className="h-full w-full object-cover"
                />
                <div className="veil absolute inset-0" />
                <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-5 pb-10">
                    <button
                        onClick={onBack}
                        className="track-wide text-[0.55rem] text-muted-foreground transition-colors hover:text-foreground"
                    >
                        ← Back to your matches
                    </button>
                    <motion.h1
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1.2, delay: 0.2, ease }}
                        className="mt-4 text-5xl text-foreground sm:text-7xl"
                    >
                        {locality.name}
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, delay: 0.35, ease }}
                        className="mt-3 max-w-xl text-sm font-light text-accent sm:text-base"
                    >
                        Rental intelligence powered by live listing activity across the locality.
                    </motion.p>
                </div>
            </div>

            <div className="mx-auto mt-12 max-w-6xl space-y-8 px-5">


                <Panel delay={0.08}>
                    <p className="track-wide text-[0.5rem] text-accent">At a Glance</p>
                    <div className="mt-5 grid gap-6 sm:grid-cols-3">
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">Average rent</p>
                            <p className="mt-2 text-3xl font-light text-foreground">
                                {locality.avgRent ? inr(locality.avgRent) : "N/A"}
                            </p>
                            <p className="mt-1 text-xs text-muted-foreground">2 BHK, semi-furnished</p>
                        </div>
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">Homes listed</p>
                            <p className="mt-2 text-3xl font-light text-foreground">
                                {locality.listingCount?.toLocaleString("en-IN") ?? "N/A"}
                            </p>
                        </div>
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">Rent range</p>
                            <p className="mt-2 text-3xl font-light text-foreground">
                                {locality.minRent !== undefined && locality.maxRent !== undefined
                                    ? `${inr(locality.minRent)} - ${inr(locality.maxRent)}`
                                    : "N/A"}
                            </p>
                            <p className="mt-1 text-xs text-muted-foreground">Backend data</p>
                        </div>
                    </div>

                    <div className="mt-8 grid gap-6 md:grid-cols-3">
                        {[
                            ["Rental Availability", locality.inventoryScore],
                            ["Neighbourhood Activity", locality.densityScore],
                            ["Overall Rental Strength", locality.overallScore],
                        ].map(([label, score]) => {
                            const percent = scorePercent(score as number | undefined) ?? 0;
                            return (
                                <div key={label as string} className="rounded-2xl border border-white/10 p-5">
                                    <p className="text-xs text-muted-foreground">{label}</p>
                                    <div className="mt-4 h-2 rounded-full bg-white/10">
                                        <div
                                            className="h-2 rounded-full bg-accent"
                                            style={{ width: `${percent}%` }}
                                        />
                                    </div>
                                    <p className="mt-3 text-sm text-muted-foreground">
                                        {Math.round(percent)}%
                                    </p>
                                </div>
                            );
                        })}
                    </div>
                </Panel>

                <Panel delay={0.1}>
                    <p className="track-wide text-[0.5rem] text-accent">Key Signals</p>
                    <div className="mt-6 grid gap-5 sm:grid-cols-3">
                        <div>
                            <p className="text-xs text-muted-foreground">Listing Inventory</p>
                            <p className="mt-2 text-lg text-foreground">
                                {locality.listingCount !== undefined
                                    ? `${locality.listingCount.toLocaleString("en-IN")} homes available`
                                    : "N/A"}
                            </p>
                        </div>
                        <div>
                            <p className="text-xs text-muted-foreground">Average Rent</p>
                            <p className="mt-2 text-lg text-foreground">
                                {locality.avgRent !== undefined ? inr(locality.avgRent) : "N/A"}
                            </p>
                        </div>
                        <div>
                            <p className="text-xs text-muted-foreground">Rental Range</p>
                            <p className="mt-2 text-lg text-foreground">
                                {locality.minRent !== undefined && locality.maxRent !== undefined
                                    ? `${inr(locality.minRent)} - ${inr(locality.maxRent)}`
                                    : "N/A"}
                            </p>
                        </div>
                    </div>
                </Panel>

                <div className="grid gap-5 md:grid-cols-5">
                    <Panel delay={0.15} className="md:col-span-3">
                        <p className="track-wide text-[0.5rem] text-accent">Explore the Area</p>
                        <p className="mt-3 text-sm font-light leading-relaxed text-muted-foreground">
                            Browse the approximate centre of this locality and explore nearby roads, landmarks and neighbourhoods.
                        </p>
                        <div className="mt-5">
                            <AreaMap locality={locality} />
                        </div>
                    </Panel>

                    <Panel delay={0.2} className="md:col-span-2">
                        <p className="track-wide text-[0.5rem] text-accent">Who Typically Likes Areas Like This?</p>
                        <div className="mt-5 flex flex-wrap gap-2.5">
                            {bestFor.map((tag) => (
                                <span
                                    key={tag}
                                    className="rounded-full bg-[image:var(--gradient-dusk)] px-4 py-2 text-xs track-wide text-primary-foreground"
                                >
                                    {tag}
                                </span>
                            ))}
                        </div>
                    </Panel>
                </div>
            </div>
        </section>
    );
}
