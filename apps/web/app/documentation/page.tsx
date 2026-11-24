"use client";

import { ApiDocs } from "@/components/billing/api-docs";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function DocumentationPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("docs_title")} subtitle={t("docs_text")} />
      <section className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
        <ApiDocs />
      </section>
    </>
  );
}
