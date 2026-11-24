/**
 * Contrats partagés entre le site web, l'application mobile et l'API.
 * Ce package ne contient aucun secret et aucune logique métier.
 */

export type RiskLevel = "low" | "medium" | "high";

export type AnalysisKind = "url" | "message";

export interface RiskIndicator {
  /** Code stable, utilisable par les clients pour mapper des traductions. */
  code: string;
  /** Libellé humain en français. */
  label: string;
  /** Explication précise de l'élément détecté. */
  detail: string;
  /** Poids indicatif utilisé par le moteur de score (0-100). */
  weight: number;
}

export interface AnalysisResult {
  id: string;
  kind: AnalysisKind;
  riskLevel: RiskLevel;
  /** Score indicatif de 0 à 100. 100 = signal le plus fort, jamais une preuve. */
  score: number;
  indicators: RiskIndicator[];
  recommendations: string[];
  limitations: string[];
  createdAt: string;
}

export const RISK_LABELS: Record<RiskLevel, string> = {
  low: "Risque faible",
  medium: "Risque moyen",
  high: "Risque élevé",
};

export const API_PREFIX = "/api/v1";

export const ANALYSIS_LIMITS = {
  urlMaxLength: 2048,
  messageMaxLength: 4000,
} as const;

import plansCatalog from "../plans.json";

export type PlanCode = "free" | "pro" | "business";

export interface PlanDefinition {
  code: PlanCode;
  name: string;
  priceLabel: string;
  dailyAnalyses: number;
  apiKeys: number;
  description: string;
  features: string[];
}

export interface PlansCatalogDefinition {
  currency: string;
  paymentActive: boolean;
  note: string;
  plans: PlanDefinition[];
}

/** Source unique des offres, partagée par le site, le mobile et l'API. */
export const PLANS = plansCatalog as PlansCatalogDefinition;

export const DEFAULT_PLAN: PlanCode = "free";
