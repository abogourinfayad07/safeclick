"use client";

import { AnalysisForm } from "@/components/analysis/analysis-form";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function AnalyzePage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("analyze_title")} subtitle={t("analyze_subtitle")} />
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <AnalysisForm />
      </div>
    </>
  );
}
