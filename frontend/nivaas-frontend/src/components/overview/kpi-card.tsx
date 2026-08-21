import { useEffect, useRef, useState } from "react";
import { motion, animate } from "framer-motion";
import type { LucideIcon } from "lucide-react";

interface KpiCardProps {
    label: string;
    value: number | null | undefined;
    icon: LucideIcon;
    suffix?: string;
    delay?: number;
}

export function KpiCard({
    label,
    value,
    icon: Icon,
    suffix = "",
    delay = 0,
}: KpiCardProps) {
    const [display, setDisplay] = useState(0);
    const previous = useRef(0);

    useEffect(() => {
        if (value == null) return;

        const controls = animate(previous.current, value, {
            duration: 1,
            onUpdate(latest) {
                setDisplay(Math.round(latest));
            },
        });

        previous.current = value;

        return () => controls.stop();
    }, [value]);

    return (
        <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay }}
            whileHover={{ y: -3 }}
            className="rounded-2xl border border-white/10 bg-white/5 p-6"
        >
            <div className="flex items-center justify-between">
                <span className="text-sm text-white/60">{label}</span>

                <Icon className="h-5 w-5 text-emerald-400" />
            </div>

            <div className="mt-4 text-3xl font-bold text-white">
                {value == null ? "—" : `${display.toLocaleString()}${suffix}`}
            </div>
        </motion.div>
    );
}

export function KpiCardSkeleton() {
    return (
        <div className="animate-pulse rounded-2xl border border-white/10 bg-white/5 p-6">
            <div className="h-4 w-24 rounded bg-white/10"></div>

            <div className="mt-5 h-8 w-20 rounded bg-white/10"></div>
        </div>
    );
}
