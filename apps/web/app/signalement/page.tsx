"use client";

import { PageHeader } from "@/components/layout/page-header";
import { ReportForm } from "@/components/reports/report-form";
import { useT } from "@/lib/i18n";

export default function ReportPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("report_title")} subtitle={t("report_subtitle")} />
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <ReportForm />
      </div>
    </>
  );
}
