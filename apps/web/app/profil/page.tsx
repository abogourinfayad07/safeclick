"use client";

import { ProfilePanel } from "@/components/dashboard/profile-panel";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function ProfilePage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("profile_title")} subtitle={t("privacy_text")} />
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <ProfilePanel />
      </div>
    </>
  );
}
