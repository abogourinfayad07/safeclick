"use client";

import { ApiKeysPanel } from "@/components/billing/api-keys-panel";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function ApiKeysPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("keys_title")} subtitle={t("keys_text")} />
      <section className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
        <ApiKeysPanel />
      </section>
    </>
  );
}
