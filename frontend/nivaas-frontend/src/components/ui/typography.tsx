import { createElement, forwardRef, type ElementType, type HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

/**
 * Typography system — every piece of text in the product should be able
 * to reach for one of these instead of ad-hoc `text-*` utility soup.
 * Keeps the display/body/mono roles (see tailwind.config.ts) applied
 * consistently across features.
 */

type TextElement = "h1" | "h2" | "h3" | "h4" | "p" | "span" | "div";

interface TypographyProps extends HTMLAttributes<HTMLElement> {
  as?: TextElement;
}

function makeTypographyComponent(defaultTag: TextElement, baseClassName: string) {
  const Component = forwardRef<HTMLElement, TypographyProps>(
    ({ as, className, ...props }, ref) => {
      const tag: ElementType = as ?? defaultTag;
      return createElement(tag, { ref, className: cn(baseClassName, className), ...props });
    },
  );
  Component.displayName = "Typography";
  return Component;
}

/** Hero-scale headline. Use once per page, at most. */
export const DisplayXL = makeTypographyComponent(
  "h1",
  "font-display text-display-lg md:text-display-xl text-text-primary",
);

/** Section-level headline. */
export const DisplayLG = makeTypographyComponent(
  "h2",
  "font-display text-display-md text-text-primary",
);

/** Subsection headline / card group title. */
export const DisplaySM = makeTypographyComponent(
  "h3",
  "font-display text-display-sm text-text-primary",
);

/** Standard paragraph copy. */
export const Text = makeTypographyComponent("p", "font-sans text-body text-text-secondary");

/** Emphasized lead paragraph, used under a headline. */
export const TextLead = makeTypographyComponent(
  "p",
  "font-sans text-body-lg text-text-secondary",
);

/** Small print — form hints, footnotes, legal text. */
export const TextSmall = makeTypographyComponent(
  "p",
  "font-sans text-body-sm text-text-tertiary",
);

/** Uppercase micro-label — eyebrows, table headers, status tags. */
export const Caption = makeTypographyComponent(
  "span",
  "font-sans text-caption uppercase tracking-wider text-text-tertiary",
);

/** Numeric/data display — rents, coordinates, percentages. Tabular figures. */
export const DataText = makeTypographyComponent(
  "span",
  "font-mono text-data font-tabular text-text-primary",
);
