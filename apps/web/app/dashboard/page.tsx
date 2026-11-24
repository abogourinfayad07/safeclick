"use client";

import { DashboardPanel } from "@/components/dashboard/dashboard-panel";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function DashboardPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("dashboard_title")} subtitle={t("dashboard_subtitle")} />
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <DashboardPanel />
      </div>
    </>
  );
}
