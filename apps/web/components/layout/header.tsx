"use client";

import Link from "next/link";
import { ShieldCheck } from "lucide-react";
import { AuthNav } from "./auth-nav";
import { useT } from "@/lib/i18n";

export function Header() {
  const t = useT();

  const navigation = [
    { label: t("nav_analyze"), href: "/analyse" },
    { label: t("nav_report"), href: "/signalement" },
    { label: t("nav_levels"), href: "/securite" },
    { label: t("nav_privacy"), href: "/confidentialite" },
    { label: t("nav_offers"), href: "/offres" },
    { label: t("nav_docs"), href: "/documentation" },
    { label: t("nav_api_keys"), href: "/cles-api" },
    { label: t("nav_admin"), href: "/admin" },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-night-950/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2 font-bold tracking-tight">
          <ShieldCheck className="h-6 w-6 text-electric-400" aria-hidden="true" />
          <span>SAFECLICK</span>
        </Link>

        <nav aria-label="Navigation principale" className="hidden items-center gap-5 lg:flex">
          {navigation.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-sm text-slate-300 transition-colors hover:text-white"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <AuthNav />
      </div>
    </header>
  );
}
