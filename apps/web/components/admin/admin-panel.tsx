"use client";

import { useCallback, useEffect, useState } from "react";
import {
  api,
  ApiClientError,
  errorMessage,
  type AdminReport,
  type AdminStats,
} from "@/lib/api";
import { StatsBars } from "@/components/dashboard/stats-bars";
import { clearToken } from "@/lib/auth";
import { useT } from "@/lib/i18n";

export function AdminPanel() {
  const t = useT();
  const [reports, setReports] = useState<AdminReport[]>([]);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setError("");
    try {
      const [list, measured] = await Promise.all([
        api.listAdminReports(undefined, 50, 0),
        api.getAdminStats(),
      ]);
      setReports(list.items);
      setStats(measured);
    } catch (cause) {
      if (cause instanceof ApiClientError && cause.status === 401) clearToken();
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function review(id: string, status: "confirmed" | "dismissed") {
    setNotice("");
    setError("");
    try {
      await api.reviewReport(id, status);
      setNotice(t("admin_reviewed"));
      await load();
    } catch (cause) {
      setError(errorMessage(cause));
    }
  }

  if (loading) return <p className="mt-8 text-sm text-slate-400">{t("common_loading")}</p>;

  return (
    <div className="mt-8 space-y-8">
      {error ? (
        <p className="rounded-lg border border-danger-500/30 bg-danger-500/10 p-3 text-sm text-red-300">
          {error}
        </p>
      ) : null}
      {notice ? (
        <p className="rounded-lg border border-safe-500/30 bg-safe-500/10 p-3 text-sm text-green-300">
          {notice}
        </p>
      ) : null}

      {stats ? (
        <section className="rounded-2xl border border-white/10 bg-night-800/50 p-6">
          <h2 className="text-lg font-semibold">{t("admin_stats")}</h2>
          <div className="mt-4 flex flex-wrap gap-6 text-sm text-slate-300">
            <span>{t("dashboard_stats_users")} : {stats.users}</span>
            <span>{t("dashboard_stats_reports")} : {Object.values(stats.reports).reduce((a, b) => a + b, 0)}</span>
            <span>{t("dashboard_stats_analyses")} : {Object.values(stats.analyses).reduce((a, b) => a + b, 0)}</span>
          </div>
          <StatsBars values={stats.reports} />
          <p className="mt-3 text-xs text-slate-500">{stats.note}</p>
        </section>
      ) : null}

      <section className="rounded-2xl border border-white/10 bg-night-800/50 p-6">
        <h2 className="text-lg font-semibold">{t("admin_reports")}</h2>
        {reports.length === 0 ? (
          <p className="mt-4 text-sm text-slate-400">{t("admin_empty")}</p>
        ) : (
          <ul className="mt-4 divide-y divide-white/10">
            {reports.map((report) => (
              <li key={report.id} className="flex flex-wrap items-center gap-4 py-4">
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-white">
                    {report.contactKind} — {report.reasonCode}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    {report.status} — {new Date(report.createdAt).toLocaleString()}
                  </p>
                </div>
                {report.status === "unverified" ? (
                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => void review(report.id, "confirmed")}
                      className="rounded-lg bg-electric-500 px-3 py-2 text-xs font-semibold text-white hover:bg-electric-400"
                    >
                      {t("admin_review_confirm")}
                    </button>
                    <button
                      type="button"
                      onClick={() => void review(report.id, "dismissed")}
                      className="rounded-lg border border-white/15 px-3 py-2 text-xs font-semibold text-slate-200 hover:bg-white/5"
                    >
                      {t("admin_review_dismiss")}
                    </button>
                  </div>
                ) : null}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
