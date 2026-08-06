import { forwardRef, type ButtonHTMLAttributes } from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

/**
 * Button — the single interactive-action primitive for NIVAAS.
 *
 * Variants map to real product meaning, not just visual flavor:
 *  - primary   → the one emphasized action in a view (signal green)
 *  - secondary → standard secondary actions
 *  - outline   → quiet actions inside dense data surfaces (tables, filters)
 *  - ghost     → lowest-emphasis, icon-adjacent actions
 *  - brass     → reserved for rare, premium moments (e.g. "Unlock full report")
 *  - destructive → irreversible actions only
 */
const buttonVariants = cva(
  [
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium",
    "transition-all duration-200 ease-instrument",
    "disabled:pointer-events-none disabled:opacity-40",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal-500 focus-visible:ring-offset-2 focus-visible:ring-offset-ink",
  ].join(" "),
  {
    variants: {
      variant: {
        primary:
          "bg-signal-500 text-white shadow-subtle hover:bg-signal-600 active:bg-signal-700",
        secondary:
          "bg-ink-overlay text-text-primary border border-line-dark hover:border-white/20 hover:bg-white/[0.04]",
        outline:
          "border border-line-dark text-text-primary hover:bg-white/[0.04] hover:border-white/20",
        ghost: "text-text-secondary hover:text-text-primary hover:bg-white/[0.04]",
        brass:
          "bg-brass-500 text-ink shadow-subtle hover:bg-brass-600 font-medium",
        destructive: "bg-danger text-white hover:bg-danger/90",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  },
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Render as the child element instead of a <button> (e.g. wrapping a <Link>) */
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp className={cn(buttonVariants({ variant, size }), className)} ref={ref} {...props} />
    );
  },
);
Button.displayName = "Button";

export { buttonVariants };
