import { Section } from "@/components/ui/section";
import { DisplaySM, Text } from "@/components/ui/typography";

/**
 * Foundation-only placeholder. Renders at every route so the shell (navbar,
 * sidebar, routing, layout) is verifiable end-to-end before any feature page
 * is built. Replace each usage with the real feature page when that page's
 * own session begins — this component holds no business logic and should
 * not be extended.
 */
export function RoutePlaceholder({ routeName }: { routeName: string }) {
  return (
    <Section
      eyebrow="Foundation scaffold"
      title={<DisplaySM>{routeName}</DisplaySM>}
      description={
        <Text>
          This route is wired into the router and layout shell. Its feature implementation is
          out of scope for the current session.
        </Text>
      }
    />
  );
}
