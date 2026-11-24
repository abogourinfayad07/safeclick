"use client";

import Link from "next/link";
import { useT } from "@/lib/i18n";

export function Footer() {
  const t = useT();

  return (
    <footer className="mt-20 border-t border-white/10 bg-night-900/50">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-sm text-slate-400 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p>{t("footer_rights")}</p>
        <nav aria-label="Navigation de pied de page" className="flex flex-wrap gap-5">
          <Link href="/confidentialite" className="hover:text-white">
            {t("nav_privacy")}
          </Link>
          <Link href="/securite" className="hover:text-white">
            {t("security_title")}
          </Link>
          <Link href="/a-propos" className="hover:text-white">
            {t("about_title")}
          </Link>
          <Link href="/offres" className="hover:text-white">
            {t("nav_offers")}
          </Link>
          <Link href="/documentation" className="hover:text-white">
            {t("nav_docs")}
          </Link>
          <Link href="/mentions-legales" className="hover:text-white">
            {t("legal_title")}
          </Link>
        </nav>
      </div>
    </footer>
  );
}
