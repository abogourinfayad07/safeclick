"use client";

import { PricingPlans } from "@/components/billing/pricing-plans";
import { PageHeader } from "@/components/layout/page-header";
import { useT } from "@/lib/i18n";

export default function OffersPage() {
  const t = useT();
  return (
    <>
      <PageHeader title={t("offers_title")} subtitle={t("offers_text")} />
      <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <PricingPlans />
      </section>
    </>
  );
}
