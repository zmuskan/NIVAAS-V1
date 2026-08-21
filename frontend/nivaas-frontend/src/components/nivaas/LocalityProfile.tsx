import { motion } from "framer-motion";
import { AreaMap } from "@/components/nivaas/AreaMap";
import { inr, type Locality } from "@/data/nivaas";
import towers from "@/assets/tower.png";
import street from "@/assets/street.png";
import courtyard from "@/assets/courtyard.png";
import metro from "@/assets/metro.png";

const ease = [0.22, 1, 0.36, 1] as const;
const heroFor: Record<string, string> = {
    indiranagar: street,
    koramangala: street,
    "hsr-layout": courtyard,
    jayanagar: courtyard,
    banashankari: courtyard,
    whitefield: towers,
    hebbal: towers,
    "electronic-city": metro,
};

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
            className={`bg-black/60 backdrop-blur-md rounded-3xl p-7 sm:p-9 ${className}`}
        >
            {children}
        </motion.div>
    );
}

function Split({ data }: { data: { label: string; share: number }[] }) {
    return (
        <div className="space-y-5">
            {data.map((d) => (
                <div key={d.label}>
                    <div className="flex items-baseline justify-between text-sm">
                        <span className="font-light text-muted-foreground">{d.label}</span>
                        <span className="text-foreground">{d.share}%</span>
                    </div>
                    <div className="mt-2 h-[3px] overflow-hidden rounded-full bg-foreground/10">
                        <motion.div
                            initial={{ width: 0 }}
                            whileInView={{ width: `${d.share}%` }}
                            viewport={{ once: true }}
                            transition={{ duration: 1.2, ease }}
                            className="h-full rounded-full bg-[image:var(--gradient-dusk)]"
                        />
                    </div>
                </div>
            ))}
        </div>
    );
}

export function LocalityProfile({
    locality,
    onBack,
}: {
    locality: Locality;
    onBack: () => void;
}) {
    const day = locality.dayInLife;
    console.log("LOCALITY DATA", locality);

    return (
        <section className="min-h-screen pb-32">
            <div className="relative h-[68vh] overflow-hidden">
                <motion.img
                    initial={{ scale: 1.14, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 2, ease }}
                    src={heroFor[locality.id] ?? courtyard}
                    alt={`${locality.name} at dusk`}
                    className="h-full w-full object-cover"
                />
                <div className="veil absolute inset-0" />
                <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-5 pb-14">
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
                        className="mt-5 text-5xl text-foreground sm:text-7xl"
                    >
                        {locality.name}
                    </motion.h1>
                    <p className="mt-3 max-w-xl text-sm font-light text-accent sm:text-base">
                        {locality.district} · {locality.rentRange}
                    </p>
                </div>
            </div>

            <div className="mx-auto mt-12 max-w-6xl space-y-6 px-5">
                <Panel>
                    <p className="track-wide text-[0.5rem] text-accent">The place</p>
                    <p className="mt-5 text-xl font-light leading-relaxed text-foreground sm:text-2xl">
                        {locality.longBlurb}
                    </p>
                </Panel>

                <Panel delay={0.05}>
                    <p className="track-wide text-[0.5rem] text-accent">Housing snapshot</p>
                    <div className="mt-7 grid gap-7 sm:grid-cols-3">
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
                                {locality.listings?.toLocaleString("en-IN") ?? "0"}
                            </p>
                            <p className="mt-1 text-xs text-muted-foreground">
                                Availability: {locality.availability.toLowerCase()}
                            </p>
                        </div>
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">Rent range</p>
                            <p className="mt-2 text-3xl font-light text-foreground">
                                {locality.rentRange}
                            </p>
                            <p className="mt-1 text-xs text-muted-foreground">1 BHK to 3 BHK</p>
                        </div>
                    </div>

                    <div className="mt-10 grid gap-6 sm:grid-cols-3">
                        <div>
                            <p className="text-xs text-muted-foreground">
                                Overall Score
                            </p>
                            <p className="text-3xl font-light">
                                {locality.overallScore ?? "N/A"}
                            </p>
                        </div>

                        <div>
                            <p className="text-xs text-muted-foreground">
                                Inventory Score
                            </p>
                            <p className="text-3xl font-light">
                                {locality.inventoryScore ?? "N/A"}
                            </p>
                        </div>

                        <div>
                            <p className="text-xs text-muted-foreground">
                                Density Score
                            </p>
                            <p className="text-3xl font-light">
                                {locality.densityScore ?? "N/A"}
                            </p>
                        </div>
                    </div>

                    <div className="mt-10 grid gap-9 md:grid-cols-3">
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">Property types</p>
                            <div className="mt-5">
                                <Split data={locality.propertyTypes} />
                            </div>
                        </div>
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">Furnishing</p>
                            <div className="mt-5">
                                <Split data={locality.furnishing} />
                            </div>
                        </div>
                        <div>
                            <p className="track-wide text-[0.5rem] text-muted-foreground">
                                Configuration mix
                            </p>
                            <div className="mt-5">
                                <Split data={locality.bhkMix} />
                            </div>
                        </div>
                    </div>
                </Panel>

                <div className="grid gap-6 md:grid-cols-5">
                    <Panel delay={0.1} className="md:col-span-3">
                        <p className="track-wide text-[0.5rem] text-accent">A day in the life</p>
                        <div className="mt-7 space-y-7">
                            {[
                                { t: "Morning", v: day.morning },
                                { t: "Workday", v: day.workday },
                                { t: "Evening", v: day.evening },
                                { t: "Weekend", v: day.weekend },
                            ].map((s) => (
                                <div key={s.t} className="border-l border-border pl-5">
                                    <p className="track-wide text-[0.5rem] text-muted-foreground">{s.t}</p>
                                    <p className="mt-2 text-base font-light leading-relaxed text-foreground">
                                        {s.v}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </Panel>

                    <Panel delay={0.15} className="md:col-span-2">
                        <p className="track-wide text-[0.5rem] text-accent">Where the homes are</p>
                        <div className="mt-6">
                            <AreaMap locality={locality} />
                        </div>
                        <p className="mt-6 track-wide text-[0.5rem] text-muted-foreground">Nearby</p>
                        <div className="mt-4 flex flex-wrap gap-2">
                            {locality.nearby.map((n) => (
                                <span
                                    key={n}
                                    className="rounded-full bg-zinc-900/80 backdrop-blur-md px-4 py-2 text-xs text-muted-foreground"
                                >
                                    {n}
                                </span>
                            ))}
                        </div>
                    </Panel>
                </div>

                <Panel delay={0.2}>
                    <p className="track-wide text-[0.5rem] text-accent">Imagine living here</p>
                    <div className="mt-7 grid gap-7 sm:grid-cols-3">
                        {locality.imagine.map((line) => (
                            <p
                                key={line}
                                className="text-lg font-light leading-relaxed text-foreground"
                            >
                                {line}
                            </p>
                        ))}
                    </div>
                </Panel>
            </div>
        </section>
    );
}
