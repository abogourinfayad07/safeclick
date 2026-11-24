"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, ApiClientError, errorMessage } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { useT } from "@/lib/i18n";

const fieldClass =
  "w-full rounded-lg border border-white/15 bg-night-900/70 px-4 py-3 text-sm text-white focus:border-electric-400 focus:outline-none focus:ring-2 focus:ring-electric-400/40";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const t = useT();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice("");
    setError("");
    setLoading(true);
    try {
      if (mode === "register") {
        const result = await api.register(email, password);
        setNotice(result.message);
      } else {
        const result = await api.login(email, password);
        setToken(result.access_token);
        router.push("/dashboard");
      }
    } catch (cause) {
      if (cause instanceof ApiClientError) {
        setError(
          cause.details.length > 0 && cause.status === 422
            ? cause.details.map((detail) => detail.message).join(" ")
            : cause.message,
        );
      } else {
        setError(errorMessage(cause));
      }
    } finally {
      setLoading(false);
    }
  }

  const other = mode === "login" ? "/inscription" : "/connexion";

  return (
    <form
      onSubmit={onSubmit}
      className="mt-8 max-w-md rounded-2xl border border-white/10 bg-night-800/50 p-6"
    >
      <label className="block">
        <span className="text-sm font-medium text-slate-200">{t("auth_email")}</span>
        <input
          className={`${fieldClass} mt-2`}
          type="email"
          required
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </label>

      <label className="mt-5 block">
        <span className="text-sm font-medium text-slate-200">{t("auth_password")}</span>
        <input
          className={`${fieldClass} mt-2`}
          type="password"
          required
          minLength={mode === "register" ? 12 : 1}
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        {mode === "register" ? (
          <span className="mt-2 block text-xs text-slate-400">{t("auth_password_hint")}</span>
        ) : null}
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
        className="mt-6 w-full rounded-lg bg-electric-500 px-6 py-3 text-sm font-semibold text-white hover:bg-electric-400 disabled:opacity-50"
      >
        {loading
          ? t("common_loading")
          : t(mode === "login" ? "auth_login_submit" : "auth_register_submit")}
      </button>

      <p className="mt-5 text-center text-sm text-slate-400">
        {t(mode === "login" ? "auth_no_account" : "auth_has_account")}{" "}
        <Link href={other} className="text-electric-300 hover:underline">
          {t(mode === "login" ? "nav_register" : "nav_login")}
        </Link>
      </p>
    </form>
  );
}

export function VerifyForm() {
  const t = useT();
  const [token, setToken] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice("");
    setError("");
    setLoading(true);
    try {
      const result = await api.verify(token.trim());
      setNotice(result.message || t("auth_verify_success"));
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={onSubmit}
      className="mt-8 max-w-xl rounded-2xl border border-white/10 bg-night-800/50 p-6"
    >
      <p className="text-sm text-slate-300">{t("auth_verify_text")}</p>
      <label className="mt-5 block">
        <span className="text-sm font-medium text-slate-200">{t("auth_token")}</span>
        <input
          className={`${fieldClass} mt-2`}
          type="text"
          required
          value={token}
          onChange={(event) => setToken(event.target.value)}
        />
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
        {loading ? t("common_loading") : t("auth_verify_submit")}
      </button>
    </form>
  );
}
