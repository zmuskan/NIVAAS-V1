import type { AxiosRequestConfig } from "axios";
import { httpClient } from "@/lib/axios-instance";

/**
 * Thin, generically-typed wrapper around the Axios instance.
 *
 * Feature modules call `apiClient.get<PropertySearchResult>("/properties/search", { params })`
 * instead of touching Axios directly — this keeps the response-unwrapping
 * (`.data`) logic in one place and gives every call site a typed return value.
 *
 * No endpoint paths live here. Each feature owns its own paths in its
 * `api.ts`, matched exactly to the real FastAPI routes.
 */
export const apiClient = {
  get: async <TResponse>(url: string, config?: AxiosRequestConfig): Promise<TResponse> => {
    const response = await httpClient.get<TResponse>(url, config);
    return response.data;
  },
  post: async <TResponse, TBody = unknown>(
    url: string,
    body?: TBody,
    config?: AxiosRequestConfig,
  ): Promise<TResponse> => {
    const response = await httpClient.post<TResponse>(url, body, config);
    return response.data;
  },
  put: async <TResponse, TBody = unknown>(
    url: string,
    body?: TBody,
    config?: AxiosRequestConfig,
  ): Promise<TResponse> => {
    const response = await httpClient.put<TResponse>(url, body, config);
    return response.data;
  },
  patch: async <TResponse, TBody = unknown>(
    url: string,
    body?: TBody,
    config?: AxiosRequestConfig,
  ): Promise<TResponse> => {
    const response = await httpClient.patch<TResponse>(url, body, config);
    return response.data;
  },
  delete: async <TResponse>(url: string, config?: AxiosRequestConfig): Promise<TResponse> => {
    const response = await httpClient.delete<TResponse>(url, config);
    return response.data;
  },
};
