"use client";

import { useState, type FormEvent } from "react";
import { api, ApiClientError, errorMessage } from "@/lib/api";
import { useT } from "@/lib/i18n";

const fieldClass =
  "w-full rounded-lg border border-white/15 bg-night-900/70 px-4 py-3 text-sm text-white focus:border-electric-400 focus:outline-none focus:ring-2 focus:ring-electric-400/40";

const reasons = [
  "urgency",
  "payment_request",
  "code_request",
  "impersonation",
  "other",
] as const;

export function ReportForm() {
  const t = useT();
  const [contactKind, setContactKind] = useState("email");
  const [contact, setContact] = useState("");
  const [reason, setReason] = useState<string>(reasons[0]);
  const [acknowledged, setAcknowledged] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice("");
    setError("");
    setLoading(true);
    try {
      const response = await api.createReport({
        contact_kind: contactKind,
        contact,
        reason_code: reason,
        acknowledge_unverified: true,
      });
      setNotice(
        response.message.includes("déjà") ? t("report_duplicate") : t("report_success"),
      );
      setContact("");
      setAcknowledged(false);
    } catch (cause) {
      setError(
        cause instanceof ApiClientError && cause.status === 422
          ? cause.details.map((detail) => detail.message).join(" ")
          : errorMessage(cause),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={onSubmit}
      className="mt-8 max-w-2xl rounded-2xl border border-white/10 bg-night-800/50 p-6"
    >
      <div className="grid gap-5 sm:grid-cols-2">
        <label className="block">
          <span className="text-sm font-medium text-slate-200">{t("report_kind_label")}</span>
          <select
            className={`${fieldClass} mt-2`}
            value={contactKind}
            onChange={(event) => setContactKind(event.target.value)}
          >
            <option value="email">E-mail</option>
            <option value="phone">Téléphone</option>
            <option value="url">URL</option>
            <option value="other">Autre</option>
          </select>
        </label>

        <label className="block">
          <span className="text-sm font-medium text-slate-200">{t("report_reason_label")}</span>
          <select
            className={`${fieldClass} mt-2`}
            value={reason}
            onChange={(event) => setReason(event.target.value)}
          >
            <option value="urgency">Urgence</option>
            <option value="payment_request">Demande d'argent</option>
            <option value="code_request">Demande de code</option>
            <option value="impersonation">Usurpation</option>
            <option value="other">Autre</option>
          </select>
        </label>
      </div>

      <label className="mt-5 block">
        <span className="text-sm font-medium text-slate-200">{t("report_contact_label")}</span>
        <input
          className={`${fieldClass} mt-2`}
          type="text"
          required
          minLength={3}
          value={contact}
          onChange={(event) => setContact(event.target.value)}
        />
      </label>

      <label className="mt-5 flex items-start gap-3 text-sm text-slate-300">
        <input
          type="checkbox"
          className="mt-1 h-4 w-4 accent-electric-500"
          required
          checked={acknowledged}
          onChange={(event) => setAcknowledged(event.target.checked)}
        />
        <span>{t("report_ack")}</span>
      </label>

      {notice ? (
        <p className="mt-5 rounded-lg border border-safe-500/30 bg-safe-500/10 p-3 text-sm text-green-300">
          {notice}
        </p>
      ) : null}
      {error ? (
        <p className="mt-5 rounded-lg border border-danger-500/30 bg-danger-500/10 p-3 text-sm text-red-300">
          {error}
        </p>
      ) : null}

      <button
        type="submit"
        disabled={loading}
        className="mt-6 rounded-lg bg-electric-500 px-6 py-3 text-sm font-semibold text-white hover:bg-electric-400 disabled:opacity-50"
      >
        {loading ? t("common_loading") : t("report_submit")}
      </button>
    </form>
  );
}
