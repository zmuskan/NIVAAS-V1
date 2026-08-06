import { forwardRef, type HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

/**
 * Card — the base surface for grouped content (stat blocks, list items,
 * form sections). `marked` adds NIVAAS's signature corner-crosshair detail
 * — a nod to survey/map markers, appropriate here because the platform is
 * fundamentally geospatial (PostGIS-backed). Use `marked` sparingly, on the
 * one or two cards per view that represent a real data point worth
 * anchoring attention to — not on every card.
 */
export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  marked?: boolean;
  interactive?: boolean;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, marked = false, interactive = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "relative rounded-lg border border-line-dark bg-ink-raised p-6",
          interactive &&
            "transition-all duration-200 ease-instrument hover:border-white/20 hover:shadow-raised cursor-pointer",
          className,
        )}
        {...props}
      >
        {marked && (
          <>
            <CornerMark className="left-2.5 top-2.5" />
            <CornerMark className="right-2.5 top-2.5 rotate-90" />
            <CornerMark className="bottom-2.5 left-2.5 -rotate-90" />
            <CornerMark className="bottom-2.5 right-2.5 rotate-180" />
          </>
        )}
        {children}
      </div>
    );
  },
);
Card.displayName = "Card";

function CornerMark({ className }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={cn("absolute h-2.5 w-2.5 text-signal-500/50", className)}
      viewBox="0 0 10 10"
      fill="none"
    >
      <path d="M0 0H10" stroke="currentColor" strokeWidth="1" />
      <path d="M0 0V10" stroke="currentColor" strokeWidth="1" />
    </svg>
  );
}

export const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col gap-1.5 mb-4", className)} {...props} />
  ),
);
CardHeader.displayName = "CardHeader";

export const CardTitle = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("font-display text-lg font-medium text-text-primary leading-snug", className)}
      {...props}
    />
  ),
);
CardTitle.displayName = "CardTitle";

export const CardDescription = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-body-sm text-text-secondary", className)} {...props} />
  ),
);
CardDescription.displayName = "CardDescription";

export const CardContent = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn(className)} {...props} />,
);
CardContent.displayName = "CardContent";

export const CardFooter = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center mt-4 pt-4 border-t border-line-dark", className)} {...props} />
  ),
);
CardFooter.displayName = "CardFooter";
