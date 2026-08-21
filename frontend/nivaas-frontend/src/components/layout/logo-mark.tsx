import { cn } from "@/lib/utils";

/**
 * NIVAAS wordmark. "निवास" (nivaas) means "residence/dwelling" in Kannada
 * and Hindi — the mark pairs that word with a single survey crosshair,
 * tying the brand back to the platform's geospatial foundation.
 */
export function LogoMark({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true">
        <circle cx="11" cy="11" r="9.25" stroke="currentColor" strokeOpacity="0.35" />
        <path d="M11 3V19" stroke="currentColor" strokeWidth="1.25" />
        <path d="M3 11H19" stroke="currentColor" strokeWidth="1.25" />
        <circle cx="11" cy="11" r="2.5" className="fill-signal-500" stroke="none" />
      </svg>
      <span className="font-display text-lg font-medium tracking-tight text-text-primary">
        NIVAAS
      </span>
    </div>
  );
}
