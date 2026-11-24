"use client";

import { useT, type TranslationKey } from "@/lib/i18n";
import { PageHeader } from "./page-header";

export function StaticPage({
  titleKey,
  textKey,
}: {
  titleKey: TranslationKey;
  textKey: TranslationKey;
}) {
  const t = useT();
  return (
    <>
      <PageHeader title={t(titleKey)} subtitle={t(textKey)} />
      <section className="mx-auto max-w-3xl px-4 py-12 sm:px-6">
        <p className="text-sm leading-relaxed text-slate-300">{t(textKey)}</p>
      </section>
    </>
  );
}
