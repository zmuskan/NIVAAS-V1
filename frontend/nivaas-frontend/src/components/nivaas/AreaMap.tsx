import { motion } from "framer-motion";
import type { Locality } from "@/data/nivaas";

export function AreaMap({ locality }: { locality: Locality }) {
    return (
        <div className="relative aspect-[4/3] w-full overflow-hidden rounded-3xl border border-border bg-[radial-gradient(circle_at_50%_50%,color-mix(in_oklab,var(--dusk)_45%,transparent),transparent_70%)]">
            <svg viewBox="0 0 100 100" className="absolute inset-0 h-full w-full">
                {Array.from({ length: 9 }).map((_, i) => (
                    <g key={i} stroke="oklch(1 0 0 / 0.07)" strokeWidth="0.25">
                        <line x1={(i + 1) * 10} y1="0" x2={(i + 1) * 10} y2="100" />
                        <line x1="0" y1={(i + 1) * 10} x2="100" y2={(i + 1) * 10} />
                    </g>
                ))}
                <path
                    d="M8 78 C 30 62, 44 58, 62 40 S 84 26, 96 18"
                    fill="none"
                    stroke="color-mix(in oklab, var(--ember) 70%, transparent)"
                    strokeWidth="0.7"
                    strokeDasharray="3 2"
                />
                <circle
                    cx="50"
                    cy="50"
                    r="30"
                    fill="none"
                    stroke="oklch(1 0 0 / 0.1)"
                    strokeWidth="0.3"
                />
            </svg>

            {(locality.clusters ?? []).map((c, i) => (
                <motion.div
                    key={c.label}
                    initial={{ opacity: 0, scale: 0.7 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.7, delay: 0.2 + i * 0.15 }}
                    style={{ left: `${c.x}%`, top: `${c.y}%` }}
                    className="absolute -translate-x-1/2 -translate-y-1/2"
                >
                    <span className="glass-soft whitespace-nowrap rounded-full px-3 py-1.5 text-[0.6rem] text-muted-foreground">
                        {c.label}
                    </span>
                </motion.div>
            ))}

            <motion.div
                initial={{ opacity: 0, scale: 0.6 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
                style={{
                left: `${locality.coords?.x ?? 50}%`,
                top: `${locality.coords?.y ?? 50}%`
                }}
                className="absolute -translate-x-1/2 -translate-y-1/2"
            >
                <span className="absolute -inset-5 animate-ping rounded-full bg-primary/25" />
                <span className="relative grid size-3 place-items-center rounded-full bg-[image:var(--gradient-dusk)] shadow-[var(--shadow-glow)]" />
            </motion.div>

            <p className="absolute bottom-4 left-5 track-wide text-[0.5rem] text-muted-foreground">
                {locality.name} · rental clusters
            </p>
        </div>
    );
}
