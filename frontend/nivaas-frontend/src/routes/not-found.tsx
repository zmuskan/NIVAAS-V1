import { Link } from "react-router-dom";
import { Compass } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DisplayLG, Text } from "@/components/ui/typography";

export function NotFoundRoute() {
  return (
    <div className="container flex min-h-[60vh] flex-col items-center justify-center text-center">
      <Compass className="mb-4 h-8 w-8 text-signal-500" aria-hidden="true" />
      <span className="font-mono text-caption uppercase tracking-wider text-text-tertiary">
        404 — off the map
      </span>
      <DisplayLG className="mt-2">This address doesn't exist in Bengaluru.</DisplayLG>
      <Text className="mt-3 max-w-md">
        The page you're looking for isn't part of the current NIVAAS console.
      </Text>
      <Button asChild className="mt-6">
        <Link to="/">Back to overview</Link>
      </Button>
    </div>
  );
}
