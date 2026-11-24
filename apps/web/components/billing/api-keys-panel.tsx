"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { hasToken } from "@/lib/auth";
import { api, errorMessage, type ApiKeyCreated, type ApiKeyItem } from "@/lib/api";
import { useT } from "@/lib/i18n";

export function ApiKeysPanel() {
  const t = useT();
  const [items, setItems] = useState<ApiKeyItem[]>([]);
  const [name, setName] = useState("");
  const [created, setCreated] = useState<ApiKeyCreated | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(true);

  async function refresh() {
    const page = await api.listApiKeys();
    setItems(page.items);
  }

  useEffect(() => {
    if (!hasToken()) {
      setAuthenticated(false);
      setLoading(false);
      return;
    }
    void refresh()
      .catch((cause: unknown) => setError(errorMessage(cause)))
      .finally(() => setLoading(false));
  }, []);

  async function create() {
    setError("");
    setCreated(null);
    try {
      const key = await api.createApiKey(name.trim());
      setCreated(key);
      setName("");
      await refresh();
    } catch (cause) {
      setError(errorMessage(cause));
    }
  }

  async function revoke(id: string) {
    setError("");
    try {
      await api.revokeApiKey(id);
      await refresh();
    } catch (cause) {
      setError(errorMessage(cause));
    }
  }

  if (!authenticated) {
    return (
      <Link href="/connexion" className="text-sm text-electric-400 hover:underline">
        {t("nav_login")}
      </Link>
    );
  }

  return (
    <div className="mt-8">
      <p className="text-sm text-slate-300">{t("keys_text")}</p>

      <div className="mt-6 flex flex-col gap-3 sm:flex-row">
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="Nom de la clé"
          maxLength={80}
          className="rounded-xl border border-white/10 bg-night-900 px-4 py-3 text-sm text-white"
        />
        <button
          type="button"
          onClick={() => void create()}
          disabled={name.trim().length < 2}
          className="rounded-xl bg-electric-500 px-5 py-3 text-sm font-semibold text-white disabled:opacity-50"
        >
          Créer une clé
        </button>
      </div>

      {error ? <p className="mt-4 text-sm text-red-300">{error}</p> : null}

      {created ? (
        <div className="mt-6 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
          <p className="text-sm font-semibold text-emerald-200">{created.notice}</p>
          <code className="mt-3 block break-all text-xs text-emerald-100">{created.key}</code>
        </div>
      ) : null}

      <div className="mt-8 overflow-x-auto">
        {loading ? (
          <p className="text-sm text-slate-400">{t("common_loading")}</p>
        ) : items.length === 0 ? (
          <p className="text-sm text-slate-400">Aucune clé API.</p>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-500">
              <tr>
                <th className="py-2">Nom</th>
                <th className="py-2">Préfixe</th>
                <th className="py-2">Quota</th>
                <th className="py-2">Utilisé</th>
                <th className="py-2"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/10">
              {items.map((item) => (
                <tr key={item.id} className="text-slate-300">
                  <td className="py-3">{item.name}</td>
                  <td className="py-3 font-mono text-xs">{item.prefix}</td>
                  <td className="py-3">{item.dailyQuota}/jour</td>
                  <td className="py-3">{item.usageCount}</td>
                  <td className="py-3 text-right">
                    {item.revokedAt ? (
                      <span className="text-xs text-slate-500">Révoquée</span>
                    ) : (
                      <button
                        type="button"
                        onClick={() => void revoke(item.id)}
                        className="text-xs text-red-300 hover:underline"
                      >
                        Révoquer
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
