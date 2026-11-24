"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { RiskBadge } from "@/components/analysis/risk-badge";
import {
  api,
  ApiClientError,
  errorMessage,
  type AnalysisHistoryItem,
} from "@/lib/api";
import { clearToken, getToken } from "@/lib/auth";
import { useT } from "@/lib/i18n";

export function HistoryList() {
  const t = useT();
  const [items, setItems] = useState<AnalysisHistoryItem[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(true);

  useEffect(() => {
    let active = true;
    if (!getToken()) {
      setAuthenticated(false);
      setLoading(false);
      return;
    }
    api
      .listAnalyses(100, 0)
      .then((page) => {
        if (active) setItems(page.items);
      })
      .catch((cause: unknown) => {
        if (!active) return;
        if (cause instanceof ApiClientError && cause.status === 401) {
          clearToken();
          setAuthenticated(false);
        }
        setError(errorMessage(cause));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  if (!authenticated) {
    return (
      <div className="mt-8 rounded-2xl border border-white/10 bg-night-800/50 p-6">
        <Link href="/connexion" className="text-sm text-electric-300 hover:underline">
          {t("nav_login")}
        </Link>
      </div>
    );
  }

  if (loading) return <p className="mt-8 text-sm text-slate-400">{t("common_loading")}</p>;

  return (
    <div className="mt-8">
      {error ? (
        <p className="mb-4 rounded-lg border border-danger-500/30 bg-danger-500/10 p-3 text-sm text-red-300">
          {error}
        </p>
      ) : null}
      {items.length === 0 ? (
        <p className="rounded-2xl border border-white/10 bg-night-800/50 p-6 text-sm text-slate-400">
          {t("history_empty")}
        </p>
      ) : (
        <div className="overflow-x-auto rounded-2xl border border-white/10 bg-night-800/50">
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">{t("history_date")}</th>
                <th className="px-4 py-3">{t("history_kind")}</th>
                <th className="px-4 py-3">{t("history_preview")}</th>
                <th className="px-4 py-3">{t("history_score")}</th>
                <th className="px-4 py-3">{t("history_level")}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/10 text-slate-200">
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="px-4 py-3 text-xs text-slate-400">
                    {new Date(item.createdAt).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 uppercase">{item.kind}</td>
                  <td className="max-w-xs truncate px-4 py-3">{item.inputPreview ?? "—"}</td>
                  <td className="px-4 py-3">{item.score}/100</td>
                  <td className="px-4 py-3">
                    <RiskBadge level={item.riskLevel} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
