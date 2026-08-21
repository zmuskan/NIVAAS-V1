/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_API_TIMEOUT_MS: string;
  readonly VITE_MAP_TILE_URL: string;
  readonly VITE_MAP_ATTRIBUTION: string;
  readonly VITE_ENABLE_QUERY_DEVTOOLS: string;
  readonly VITE_APP_ENV: "development" | "staging" | "production";
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
