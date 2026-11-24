"use client";

import { useState, type FormEvent } from "react";
import type { AnalysisResult } from "@safeclick/shared";
import { ANALYSIS_LIMITS } from "@safeclick/shared";
import { api, errorMessage } from "@/lib/api";
import { useT } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { ResultCard } from "./result-card";

const fieldClass =
  "w-full rounded-lg border border-white/15 bg-night-900/70 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-electric-400 focus:outline-none focus:ring-2 focus:ring-electric-400/40";

type Tab = "url" | "message";

export function AnalysisForm() {
  const t = useT();
  const [tab, setTab] = useState<Tab>("url");
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data =
        tab === "url" ? await api.analyzeUrl(url) : await api.analyzeMessage(message);
      setResult(data);
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form
        onSubmit={onSubmit}
        className="mt-8 rounded-2xl border border-white/10 bg-night-800/50 p-6"
      >
        <div className="flex gap-2" role="tablist" aria-label={t("analyze_title")}>
          {(["url", "message"] as const).map((item) => (
            <button
              key={item}
              type="button"
              role="tab"
              aria-selected={tab === item}
              onClick={() => {
                setTab(item);
                setResult(null);
                setError("");
              }}
              className={cn(
                "rounded-lg px-4 py-2 text-sm font-semibold transition-colors",
                tab === item
                  ? "bg-electric-500 text-white"
                  : "border border-white/15 text-slate-300 hover:bg-white/5",
              )}
            >
              {t(item === "url" ? "analyze_tab_url" : "analyze_tab_message")}
            </button>
          ))}
        </div>

        <div className="mt-6">
          {tab === "url" ? (
            <label className="block">
              <span className="text-sm font-medium text-slate-200">
                {t("analyze_url_label")}
              </span>
              <input
                className={cn(fieldClass, "mt-2")}
                type="text"
                inputMode="url"
                required
                maxLength={ANALYSIS_LIMITS.urlMaxLength}
                value={url}
                onChange={(event) => setUrl(event.target.value)}
                placeholder={t("analyze_url_placeholder")}
              />
            </label>
          ) : (
            <label className="block">
              <span className="text-sm font-medium text-slate-200">
                {t("analyze_message_label")}
              </span>
              <textarea
                className={cn(fieldClass, "mt-2 min-h-40")}
                required
                maxLength={ANALYSIS_LIMITS.messageMaxLength}
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder={t("analyze_message_placeholder")}
              />
            </label>
          )}
        </div>

        {error ? (
          <p className="mt-4 rounded-lg border border-danger-500/30 bg-danger-500/10 p-3 text-sm text-red-300">
            {error}
          </p>
        ) : null}

        <button
          type="submit"
          disabled={loading}
          className="mt-6 rounded-lg bg-electric-500 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-electric-400 disabled:opacity-50"
        >
          {loading ? t("common_loading") : t("analyze_submit")}
        </button>
      </form>

      {result ? <ResultCard result={result} /> : null}
    </>
  );
}
