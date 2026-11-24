"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { RiskBadge } from "@/components/analysis/risk-badge";
import { StatsBars } from "@/components/dashboard/stats-bars";
import {
  api,
  ApiClientError,
  errorMessage,
  type AnalysisHistoryItem,
  type AdminStats,
  type UserProfile,
} from "@/lib/api";
import { clearToken, getToken } from "@/lib/auth";
import { useT } from "@/lib/i18n";

export function DashboardPanel() {
  const t = useT();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [items, setItems] = useState<AnalysisHistoryItem[]>([]);
  const [stats, setStats] = useState<AdminStats | null>(null);
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

    async function load() {
      try {
        const current = await api.getProfile();
        if (!active) return;
        setProfile(current);

        const history = await api.listAnalyses(5, 0);
        if (!active) return;
        setItems(history.items);

        if (current.role === "admin") {
          const measured = await api.getAdminStats();
          if (active) setStats(measured);
        }
      } catch (cause) {
        if (!active) return;
        if (cause instanceof ApiClientError && cause.status === 401) {
          clearToken();
          setAuthenticated(false);
        }
        setError(errorMessage(cause));
      } finally {
        if (active) setLoading(false);
      }
    }

    void load();
    return () => {
      active = false;
    };
  }, []);

  if (!authenticated) {
    return (
      <div className="mt-8 rounded-2xl border border-white/10 bg-night-800/50 p-6">
        <p className="text-sm text-slate-300">{t("auth_login_title")}</p>
        <Link href="/connexion" className="mt-3 inline-block text-electric-300 hover:underline">
          {t("nav_login")}
        </Link>
      </div>
    );
  }

  if (loading) return <p className="mt-8 text-sm text-slate-400">{t("common_loading")}</p>;

  return (
    <div className="mt-8 space-y-8">
      {error ? (
        <p className="rounded-lg border border-danger-500/30 bg-danger-500/10 p-3 text-sm text-red-300">
          {error}
        </p>
      ) : null}

      {profile ? (
        <section className="rounded-2xl border border-white/10 bg-night-800/50 p-6">
          <p className="text-sm text-slate-400">{t("profile_email")}</p>
          <p className="mt-1 font-semibold text-white">{profile.email}</p>
        </section>
      ) : null}

      {stats ? (
        <section className="grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-night-800/50 p-5">
            <p className="text-sm text-slate-400">{t("dashboard_stats_users")}</p>
            <p className="mt-2 text-3xl font-bold text-white">{stats.users}</p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-night-800/50 p-5">
            <p className="text-sm text-slate-400">{t("dashboard_stats_reports")}</p>
            <p className="mt-2 text-3xl font-bold text-white">
              {Object.values(stats.reports).reduce((sum, value) => sum + value, 0)}
            </p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-night-800/50 p-5">
            <p className="text-sm text-slate-400">{t("dashboard_stats_analyses")}</p>
            <p className="mt-2 text-3xl font-bold text-white">
              {Object.values(stats.analyses).reduce((sum, value) => sum + value, 0)}
            </p>
          </div>
          <div className="sm:col-span-3">
            <h3 className="text-sm font-semibold text-slate-200">{t("analyze_result_title")}</h3>
            <StatsBars values={stats.analyses} />
          </div>
          <p className="text-xs text-slate-500 sm:col-span-3">{stats.note}</p>
        </section>
      ) : null}

      <section className="rounded-2xl border border-white/10 bg-night-800/50 p-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-lg font-semibold">{t("dashboard_history")}</h2>
          <Link href="/historique" className="text-sm text-electric-300 hover:underline">
            {t("dashboard_view_all")}
          </Link>
        </div>
        {items.length === 0 ? (
          <p className="mt-4 text-sm text-slate-400">{t("dashboard_empty")}</p>
        ) : (
          <ul className="mt-4 divide-y divide-white/10">
            {items.map((item) => (
              <li key={item.id} className="flex flex-wrap items-center gap-3 py-3">
                <span className="w-16 text-xs uppercase text-slate-500">{item.kind}</span>
                <span className="min-w-0 flex-1 truncate text-sm text-slate-200">
                  {item.inputPreview ?? "—"}
                </span>
                <span className="text-sm text-white">{item.score}/100</span>
                <RiskBadge level={item.riskLevel} />
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
