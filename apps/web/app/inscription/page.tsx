"use client";

import { AuthForm } from "@/components/auth/auth-form";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function RegisterPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("auth_register_title")} subtitle={t("auth_password_hint")} />
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
        <AuthForm mode="register" />
      </div>
    </>
  );
}
