import type { HTMLAttributes, ReactNode } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

/**
 * Section — the standard vertical-rhythm wrapper every page-level block
 * uses. Handles consistent spacing, optional survey-grid backdrop, an
 * "eyebrow" label set in mono (echoing lat/long-style data labels), and a
 * gentle scroll-triggered reveal. Building a page = composing Sections,
 * not hand-spacing divs.
 */
export interface SectionProps extends HTMLAttributes<HTMLElement> {
  /** Small mono label above the title, e.g. "12.9716° N, 77.5946° E" or "03 — METHODOLOGY" */
  eyebrow?: string;
  title?: ReactNode;
  description?: ReactNode;
  /** Applies the faint cartographic grid backdrop — use on hero/divider sections only */
  grid?: boolean;
  /** Disables the scroll-reveal animation, e.g. for above-the-fold content */
  animate?: boolean;
  containerClassName?: string;
}

export function Section({
  eyebrow,
  title,
  description,
  grid = false,
  animate = true,
  className,
  containerClassName,
  children,
  ...props
}: SectionProps) {
  const content = (
    <div className={cn("container", containerClassName)}>
      {(eyebrow || title || description) && (
        <div className="mb-10 max-w-2xl">
          {eyebrow && (
            <span className="font-mono text-data uppercase tracking-wider text-signal-500">
              {eyebrow}
            </span>
          )}
          {title && (
            <h2 className="mt-2 text-display-sm md:text-display-md text-text-primary">{title}</h2>
          )}
          {description && <p className="mt-3 text-body-lg text-text-secondary">{description}</p>}
        </div>
      )}
      {children}
    </div>
  );

  return (
    <section className={cn("py-18 relative", grid && "bg-grid-signature", className)} {...props}>
      {animate ? (
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          {content}
        </motion.div>
      ) : (
        content
      )}
    </section>
  );
}
