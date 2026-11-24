"use client";

import { AuthForm } from "@/components/auth/auth-form";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function LoginPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("auth_login_title")} subtitle={t("common_disclaimer")} />
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <AuthForm mode="login" />
      </div>
    </>
  );
}
