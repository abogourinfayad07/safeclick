"use client";

import {
  API_PREFIX,
  type AnalysisKind,
  type AnalysisResult,
  type RiskLevel,
} from "@safeclick/shared";
import { getToken } from "./auth";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface ApiErrorDetail {
  field: string;
  message: string;
}

export class ApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: ApiErrorDetail[];

  constructor(
    status: number,
    code: string,
    message: string,
    details: ApiErrorDetail[] = [],
  ) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

function errorMessage(error: unknown): string {
  if (error instanceof ApiClientError) return error.message;
  return "Service indisponible.";
}

export { errorMessage };

async function request<T>(
  path: string,
  init: RequestInit = {},
  authenticated = false,
): Promise<T> {
  const headers = new Headers(init.headers);
  if (init.body !== undefined && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (authenticated) {
    const token = getToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }

  let response: Response;
  try {
    response = await fetch(`${API_URL}${API_PREFIX}${path}`, {
      ...init,
      headers,
      cache: "no-store",
    });
  } catch {
    throw new ApiClientError(0, "network_error", "Service indisponible.");
  }

  if (response.status === 204) return undefined as T;

  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const body = (payload ?? {}) as {
      code?: string;
      message?: string;
      details?: ApiErrorDetail[];
    };
    throw new ApiClientError(
      response.status,
      body.code ?? "request_rejected",
      body.message ?? "Requête refusée.",
      Array.isArray(body.details) ? body.details : [],
    );
  }
  return payload as T;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface RegisterResponse {
  email: string;
  message: string;
  verification_required: boolean;
}

export interface ReportCreated {
  id: string;
  status: string;
  created_at: string;
  message: string;
  disclaimer: string;
}

export interface UserProfile {
  email: string;
  role: string;
  isVerified: boolean;
  createdAt: string;
}

export interface AnalysisHistoryItem {
  id: string;
  kind: AnalysisKind;
  riskLevel: RiskLevel;
  score: number;
  inputPreview: string | null;
  engineVersion: string;
  createdAt: string;
}

export interface PageResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface AdminReport {
  id: string;
  contactKind: string;
  reasonCode: string;
  status: string;
  createdAt: string;
  reviewedAt: string | null;
}

export interface AdminStats {
  users: number;
  reports: Record<string, number>;
  analyses: Record<string, number>;
  note: string;
}

export interface ApiKeyCreated {
  id: string;
  name: string;
  prefix: string;
  key: string;
  dailyQuota: number;
  createdAt: string;
  notice: string;
}

export interface ApiKeyItem {
  id: string;
  name: string;
  prefix: string;
  dailyQuota: number;
  usageCount: number;
  createdAt: string;
  revokedAt: string | null;
}

export interface Subscription {
  plan: string;
  planName: string;
  paymentActive: boolean;
  note: string;
}

export const api = {
  analyzeUrl: (url: string) =>
    request<AnalysisResult>("/analyze/url", {
      method: "POST",
      body: JSON.stringify({ url }),
    }, true),

  analyzeMessage: (message: string) =>
    request<AnalysisResult>("/analyze/message", {
      method: "POST",
      body: JSON.stringify({ message }),
    }, true),

  createReport: (payload: {
    contact_kind: string;
    contact: string;
    reason_code: string;
    acknowledge_unverified: true;
  }) =>
    request<ReportCreated>("/reports", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  register: (email: string, password: string) =>
    request<RegisterResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  verify: (token: string) =>
    request<RegisterResponse>("/auth/verify", {
      method: "POST",
      body: JSON.stringify({ token }),
    }),

  login: (email: string, password: string) =>
    request<TokenResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  getProfile: () => request<UserProfile>("/user/profile", {}, true),
  deleteProfile: () =>
    request<void>("/user/profile", { method: "DELETE" }, true),

  listAnalyses: (limit = 20, offset = 0) =>
    request<PageResponse<AnalysisHistoryItem>>(
      `/analyses?limit=${limit}&offset=${offset}`,
      {},
      true,
    ),

  listAdminReports: (status?: string, limit = 20, offset = 0) => {
    const query = new URLSearchParams({ limit: String(limit), offset: String(offset) });
    if (status) query.set("status", status);
    return request<PageResponse<AdminReport>>(
      `/admin/reports?${query.toString()}`,
      {},
      true,
    );
  },

  reviewReport: (id: string, status: "confirmed" | "dismissed") =>
    request<AdminReport>(`/admin/reports/${encodeURIComponent(id)}/review`, {
      method: "POST",
      body: JSON.stringify({ status }),
    }, true),

  getAdminStats: () => request<AdminStats>("/admin/stats", {}, true),

  getSubscription: () => request<Subscription>("/billing/subscription", {}, true),
  listApiKeys: () =>
    request<{ items: ApiKeyItem[] }>("/api-keys", {}, true),
  createApiKey: (name: string) =>
    request<ApiKeyCreated>("/api-keys", {
      method: "POST",
      body: JSON.stringify({ name }),
    }, true),
  revokeApiKey: (id: string) =>
    request<void>(`/api-keys/${encodeURIComponent(id)}`, { method: "DELETE" }, true),
};
