import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { env } from "@/config/env";

/**
 * Single Axios instance for the whole app. Feature-level API modules
 * (e.g. src/features/property-search/api.ts) import this instance rather
 * than constructing their own — that keeps base URL, timeout, auth
 * header injection, and error normalization in exactly one place.
 *
 * This file intentionally defines no request functions or endpoint paths:
 * those belong to each feature's own `api.ts`, once that feature is built.
 */
export const httpClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: env.apiTimeoutMs,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor — placeholder hook for auth token injection.
// Left inert until an auth strategy exists; do not invent one here.
httpClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem("nivaas_access_token");
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }
  return config;
});

/** Normalized shape every part of the app can rely on when a request fails. */
export interface ApiErrorShape {
  status: number | null;
  message: string;
  detail?: unknown;
}

httpClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ message?: string; detail?: unknown }>) => {
    const normalized: ApiErrorShape = {
      status: error.response?.status ?? null,
      message:
        error.response?.data?.message ??
        (error.code === "ECONNABORTED"
          ? "The request timed out. Please try again."
          : "Something went wrong reaching NIVAAS services."),
      detail: error.response?.data?.detail,
    };
    return Promise.reject(normalized);
  },
);
