"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { clearToken, getToken } from "@/lib/auth";
import { useT } from "@/lib/i18n";

export function AuthNav() {
  const t = useT();
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    setLoggedIn(getToken() !== null);
  }, []);

  return (
    <div className="flex items-center gap-3">
      {loggedIn ? (
        <>
          <Link href="/dashboard" className="text-sm text-slate-300 hover:text-white">
            {t("nav_dashboard")}
          </Link>
          <button
            type="button"
            onClick={() => {
              clearToken();
              setLoggedIn(false);
              router.push("/");
            }}
            className="rounded-lg border border-white/15 px-3 py-1.5 text-xs font-semibold text-white hover:bg-white/10"
          >
            {t("nav_logout")}
          </button>
        </>
      ) : (
        <Link
          href="/connexion"
          className="rounded-lg border border-white/15 px-3 py-1.5 text-xs font-semibold text-white hover:bg-white/10"
        >
          {t("nav_login")}
        </Link>
      )}
    </div>
  );
}
