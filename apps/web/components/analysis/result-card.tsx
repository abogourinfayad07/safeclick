"use client";

import type { AnalysisResult } from "@safeclick/shared";
import { RiskBadge } from "@/components/analysis/risk-badge";
import { useT } from "@/lib/i18n";

export function ResultCard({ result }: { result: AnalysisResult }) {
  const t = useT();

  return (
    <section className="mt-8 rounded-2xl border border-white/10 bg-night-800/50 p-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h2 className="text-xl font-semibold">{t("analyze_result_title")}</h2>
        <RiskBadge level={result.riskLevel} />
      </div>

      <div className="mt-6">
        <div className="flex items-baseline justify-between text-sm text-slate-300">
          <span>{t("analyze_score")}</span>
          <span className="text-2xl font-bold text-white">{result.score}/100</span>
        </div>
        <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full bg-electric-500"
            style={{ width: `${result.score}%` }}
            role="meter"
            aria-valuenow={result.score}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={t("analyze_score")}
          />
        </div>
      </div>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-electric-300">
            {t("analyze_indicators")}
          </h3>
          {result.indicators.length === 0 ? (
            <p className="mt-3 text-sm text-slate-400">{t("analyze_no_indicators")}</p>
          ) : (
            <ul className="mt-3 space-y-3">
              {result.indicators.map((indicator) => (
                <li
                  key={indicator.code}
                  className="rounded-lg border border-white/10 bg-night-900/60 p-3"
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-sm font-semibold text-white">{indicator.label}</span>
                    <span className="text-xs text-slate-400">+{indicator.weight}</span>
                  </div>
                  <p className="mt-1 text-sm leading-relaxed text-slate-300">
                    {indicator.detail}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-electric-300">
              {t("analyze_recommendations")}
            </h3>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-300">
              {result.recommendations.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-electric-300">
              {t("analyze_limitations")}
            </h3>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-400">
              {result.limitations.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <p className="mt-8 border-t border-white/10 pt-4 text-xs text-slate-500">
        {t("common_disclaimer")}
      </p>
    </section>
  );
}
