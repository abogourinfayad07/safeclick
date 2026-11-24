import {
  API_PREFIX,
  type AnalysisKind,
  type AnalysisResult,
  type RiskLevel,
} from "@safeclick/shared";
import { getToken } from "./token";

export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, code: string, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

export function errorMessage(error: unknown): string {
  return error instanceof ApiError ? error.message : "Service indisponible.";
}

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
    const token = await getToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }

  let response: Response;
  try {
    response = await fetch(`${API_URL}${API_PREFIX}${path}`, { ...init, headers });
  } catch {
    throw new ApiError(0, "network_error", "Service indisponible.");
  }

  if (response.status === 204) return undefined as T;
  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const body = (payload ?? {}) as { code?: string; message?: string };
    throw new ApiError(
      response.status,
      body.code ?? "request_rejected",
      body.message ?? "Requête refusée.",
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

export interface HistoryItem {
  id: string;
  kind: AnalysisKind;
  riskLevel: RiskLevel;
  score: number;
  inputPreview: string | null;
  engineVersion: string;
  createdAt: string;
}

export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
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
  deleteProfile: () => request<void>("/user/profile", { method: "DELETE" }, true),
  listAnalyses: (limit = 50, offset = 0) =>
    request<Page<HistoryItem>>(`/analyses?limit=${limit}&offset=${offset}`, {}, true),
};
