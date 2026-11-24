"use client";

import Link from "next/link";
import { ArrowRight, Link2, MessageSquare, ShieldCheck } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { RiskBadge } from "@/components/analysis/risk-badge";
import { useT } from "@/lib/i18n";

export default function HomePage() {
  const t = useT();

  const features = [
    {
      icon: Link2,
      title: t("feature_link_title"),
      description: t("feature_link_text"),
    },
    {
      icon: MessageSquare,
      title: t("feature_message_title"),
      description: t("feature_message_text"),
    },
    {
      icon: ShieldCheck,
      title: t("feature_report_title"),
      description: t("feature_report_text"),
    },
  ];

  return (
    <>
      <section className="relative overflow-hidden border-b border-white/10">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_50%_0%,rgba(37,99,235,0.18),transparent_60%)]" />
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-electric-300">
            {t("home_eyebrow")}
          </p>
          <h1 className="max-w-3xl text-4xl font-bold leading-tight tracking-tight sm:text-6xl">
            {t("home_title")}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-slate-300">
            {t("home_subtitle")}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/analyse" className={buttonVariants({ size: "lg" })}>
              {t("home_cta")} <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <Link
              href="/confidentialite"
              className={buttonVariants({ variant: "outline", size: "lg" })}
            >
              {t("home_privacy_cta")}
            </Link>
          </div>
          <p className="mt-5 text-xs text-slate-500">{t("security_text")}</p>
        </div>
      </section>

      <section id="mission" className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold sm:text-3xl">{t("home_mission_title")}</h2>
        <p className="mt-4 max-w-3xl leading-relaxed text-slate-300">
          {t("home_mission_text")}
        </p>
      </section>

      <section id="fonctionnalites" className="border-y border-white/10 bg-night-900/40">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
          <h2 className="text-2xl font-bold sm:text-3xl">{t("home_features_title")}</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            {features.map((feature) => (
              <article
                key={feature.title}
                className="rounded-2xl border border-white/10 bg-night-800/50 p-6"
              >
                <feature.icon className="h-7 w-7 text-electric-400" aria-hidden="true" />
                <h3 className="mt-4 text-lg font-semibold">{feature.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-300">
                  {feature.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="niveaux" className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold sm:text-3xl">{t("home_levels_title")}</h2>
        <div className="mt-8 flex flex-wrap items-center gap-4">
          <RiskBadge level="low" />
          <RiskBadge level="medium" />
          <RiskBadge level="high" />
        </div>
        <p className="mt-5 max-w-3xl text-sm leading-relaxed text-slate-300">
          {t("home_levels_text")} <strong className="text-white">{t("common_disclaimer")}</strong>
        </p>
      </section>

      <section id="confidentialite" className="border-t border-white/10 bg-night-900/40">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
          <h2 className="text-2xl font-bold sm:text-3xl">{t("home_privacy_title")}</h2>
          <p className="mt-4 max-w-3xl leading-relaxed text-slate-300">
            {t("home_privacy_text")}
          </p>
        </div>
      </section>
    </>
  );
}
