"use client";

import { API_PREFIX } from "@safeclick/shared";
import { API_URL } from "@/lib/api";
import { useT } from "@/lib/i18n";

const example = `curl -X POST "${API_URL}${API_PREFIX}/analyze/url" \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: sc_exemple_a_remplacer" \\
  -d '{"url":"https://exemple.fr/page"}'`;

export function ApiDocs() {
  const t = useT();

  return (
    <div className="mt-8 space-y-8 text-sm leading-relaxed text-slate-300">
      <p>{t("docs_text")}</p>

      <section>
        <h2 className="text-lg font-semibold text-white">Base URL</h2>
        <code className="mt-2 block rounded-xl bg-black/30 p-4 text-xs text-electric-300">
          {API_URL}
          {API_PREFIX}
        </code>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-white">Endpoints publics</h2>
        <ul className="mt-3 space-y-2 font-mono text-xs">
          <li>GET /health</li>
          <li>GET /api/v1/info</li>
          <li>GET /api/v1/billing/plans</li>
          <li>POST /api/v1/reports</li>
          <li>POST /api/v1/analyze/url</li>
          <li>POST /api/v1/analyze/message</li>
        </ul>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-white">Analyse avec clé API</h2>
        <pre className="mt-3 overflow-x-auto rounded-xl bg-black/30 p-4 text-xs text-emerald-200">
          {example}
        </pre>
        <p className="mt-3 text-xs text-slate-500">
          La clé est affichée une seule fois dans votre espace. Aucune clé réelle ne figure dans cette documentation.
        </p>
      </section>

      <section>
        <h2 className="text-lg font-semibold text-white">Réponse et limites</h2>
        <p>
          Chaque réponse contient un niveau de risque, un score indicatif, des indicateurs explicables, des recommandations et des limites. Aucun lien soumis n&apos;est visité par le serveur.
        </p>
        <p className="mt-2">
          Les erreurs utilisent un format JSON uniforme avec un code stable. Le code{" "}
          <code className="text-electric-300">quota_exceeded</code> indique un quota journalier épuisé.
        </p>
      </section>
    </div>
  );
}
