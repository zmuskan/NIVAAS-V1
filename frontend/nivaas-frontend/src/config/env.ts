/**
 * Centralized, typed access to environment configuration.
 *
 * Nothing outside this file should read `import.meta.env` directly —
 * that keeps every env variable validated once, at boot, instead of
 * failing silently deep inside a feature module.
 */

interface AppConfig {
  apiBaseUrl: string;
  apiTimeoutMs: number;
  map: {
    tileUrl: string;
    attribution: string;
  };
  enableQueryDevtools: boolean;
  appEnv: "development" | "staging" | "production";
}

function requireEnv(key: keyof ImportMetaEnv): string {
  const value = import.meta.env[key];
  if (!value) {
    throw new Error(
      `[env] Missing required environment variable: ${key}. Check your .env.local against .env.example.`,
    );
  }
  return value;
}

function parseBoolean(value: string | undefined, fallback: boolean): boolean {
  if (value === undefined) return fallback;
  return value.toLowerCase() === "true";
}

export const env: AppConfig = {
  apiBaseUrl: requireEnv("VITE_API_BASE_URL"),
  apiTimeoutMs: Number(import.meta.env.VITE_API_TIMEOUT_MS) || 15_000,
  map: {
    tileUrl: requireEnv("VITE_MAP_TILE_URL"),
    attribution: import.meta.env.VITE_MAP_ATTRIBUTION || "© OpenStreetMap contributors",
  },
  enableQueryDevtools: parseBoolean(import.meta.env.VITE_ENABLE_QUERY_DEVTOOLS, false),
  appEnv: (import.meta.env.VITE_APP_ENV as AppConfig["appEnv"]) || "development",
};
