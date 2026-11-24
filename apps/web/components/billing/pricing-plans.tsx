"use client";

import { PLANS } from "@safeclick/shared";
import { useT } from "@/lib/i18n";

export function PricingPlans() {
  const t = useT();

  return (
    <>
      <p className="text-sm leading-relaxed text-slate-300">{t("offers_text")}</p>
      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {PLANS.plans.map((plan) => (
          <section
            key={plan.code}
            className="rounded-2xl border border-white/10 bg-night-900/70 p-6"
          >
            <p className="text-xs font-semibold uppercase tracking-widest text-electric-400">
              {plan.name}
            </p>
            <p className="mt-3 text-2xl font-bold text-white">{plan.priceLabel}</p>
            <p className="mt-3 text-sm text-slate-400">{plan.description}</p>
            <dl className="mt-5 space-y-2 text-sm">
              <div className="flex justify-between gap-3">
                <dt className="text-slate-400">Analyses / jour</dt>
                <dd className="font-semibold text-white">
                  {plan.dailyAnalyses.toLocaleString("fr-FR")}
                </dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-slate-400">Clés API</dt>
                <dd className="font-semibold text-white">{plan.apiKeys}</dd>
              </div>
            </dl>
            <ul className="mt-5 space-y-2 text-sm text-slate-300">
              {plan.features.map((feature) => (
                <li key={feature}>• {feature}</li>
              ))}
            </ul>
          </section>
        ))}
      </div>
      <p className="mt-6 text-xs text-slate-500">{PLANS.note}</p>
    </>
  );
}
