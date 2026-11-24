"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, ApiClientError, errorMessage, type UserProfile } from "@/lib/api";
import { clearToken, getToken } from "@/lib/auth";
import { useT } from "@/lib/i18n";

export function ProfilePanel() {
  const t = useT();
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [error, setError] = useState("");
  const [confirming, setConfirming] = useState(false);
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
      .getProfile()
      .then((data) => {
        if (active) setProfile(data);
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

  async function removeAccount() {
    setError("");
    try {
      await api.deleteProfile();
      clearToken();
      router.push("/");
    } catch (cause) {
      setError(errorMessage(cause));
    }
  }

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
    <div className="mt-8 max-w-2xl space-y-6">
      {error ? (
        <p className="rounded-lg border border-danger-500/30 bg-danger-500/10 p-3 text-sm text-red-300">
          {error}
        </p>
      ) : null}
      {profile ? (
        <dl className="rounded-2xl border border-white/10 bg-night-800/50 p-6 text-sm">
          <div className="flex justify-between gap-4 border-b border-white/10 py-3">
            <dt className="text-slate-400">{t("profile_email")}</dt>
            <dd className="text-white">{profile.email}</dd>
          </div>
          <div className="flex justify-between gap-4 border-b border-white/10 py-3">
            <dt className="text-slate-400">{t("profile_role")}</dt>
            <dd className="text-white">{profile.role}</dd>
          </div>
          <div className="flex justify-between gap-4 border-b border-white/10 py-3">
            <dt className="text-slate-400">{t("profile_verified")}</dt>
            <dd className="text-white">{String(profile.isVerified)}</dd>
          </div>
          <div className="flex justify-between gap-4 py-3">
            <dt className="text-slate-400">{t("profile_created")}</dt>
            <dd className="text-white">{new Date(profile.createdAt).toLocaleString()}</dd>
          </div>
        </dl>
      ) : null}

      <section className="rounded-2xl border border-danger-500/30 bg-danger-500/5 p-6">
        <p className="text-sm text-slate-300">{t("profile_delete_warning")}</p>
        {confirming ? (
          <div className="mt-4 flex gap-3">
            <button
              type="button"
              onClick={() => void removeAccount()}
              className="rounded-lg bg-danger-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500"
            >
              {t("profile_delete_confirm")}
            </button>
            <button
              type="button"
              onClick={() => setConfirming(false)}
              className="rounded-lg border border-white/15 px-4 py-2 text-sm text-slate-200 hover:bg-white/5"
            >
              {t("common_cancel")}
            </button>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => setConfirming(true)}
            className="mt-4 rounded-lg border border-danger-500/40 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-danger-500/10"
          >
            {t("profile_delete")}
          </button>
        )}
      </section>
    </div>
  );
}
