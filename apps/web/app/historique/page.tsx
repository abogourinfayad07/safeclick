"use client";

import { HistoryList } from "@/components/dashboard/history-list";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function HistoryPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("history_title")} subtitle={t("common_disclaimer")} />
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <HistoryList />
      </div>
    </>
  );
}
