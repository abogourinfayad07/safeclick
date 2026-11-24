"use client";

import { AdminPanel } from "@/components/admin/admin-panel";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function AdminPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("admin_title")} subtitle={t("admin_reports")} />
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <AdminPanel />
      </div>
    </>
  );
}
