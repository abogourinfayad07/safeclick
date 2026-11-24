"use client";

import { VerifyForm } from "@/components/auth/auth-form";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function VerifyPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("auth_verify_title")} subtitle={t("auth_verify_text")} />
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <VerifyForm />
      </div>
    </>
  );
}
