import Link from "next/link";
import { ShieldCheck } from "lucide-react";

const navigation = [
  { label: "Mission", href: "#mission" },
  { label: "Fonctionnalités", href: "#fonctionnalites" },
  { label: "Niveaux de risque", href: "#niveaux" },
  { label: "Confidentialité", href: "#confidentialite" },
];

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-night-950/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="#mission" className="flex items-center gap-2 font-bold tracking-tight">
          <ShieldCheck className="h-6 w-6 text-electric-400" aria-hidden="true" />
          <span>SAFECLICK</span>
        </Link>

        <nav aria-label="Navigation principale" className="hidden items-center gap-6 md:flex">
          {navigation.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-sm text-slate-300 transition-colors hover:text-white"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <a
          href="#fonctionnalites"
          className="rounded-lg border border-white/15 px-3 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-white/10"
        >
          Découvrir
        </a>
      </div>
    </header>
  );
}
