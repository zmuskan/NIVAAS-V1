import { QueryClient } from "@tanstack/react-query";
import type { ApiErrorShape } from "@/lib/axios-instance";

/**
 * Central TanStack Query client. Defaults are tuned for a data-heavy
 * analytics product: rent/analytics data doesn't change every second,
 * so we favor cache reuse over aggressive refetching, but we do retry
 * network blips once before surfacing an error.
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute — analytics data is not real-time
      gcTime: 5 * 60 * 1000, // keep unused cache for 5 minutes
      refetchOnWindowFocus: false,
      retry: (failureCount, error) => {
        const apiError = error as ApiErrorShape;
        // Don't retry client errors (4xx) — retry only network/5xx issues
        if (apiError.status && apiError.status >= 400 && apiError.status < 500) {
          return false;
        }
        return failureCount < 2;
      },
    },
    mutations: {
      retry: false,
    },
  },
});
