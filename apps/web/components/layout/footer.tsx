export function Footer() {
  return (
    <footer className="mt-20 border-t border-white/10 bg-night-900/50">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-sm text-slate-400 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p>© 2026 SAFECLICK — Développé au Bénin pour l’Afrique francophone.</p>
        <div className="flex gap-5">
          <a href="#confidentialite" className="hover:text-white">Confidentialité</a>
          <a href="#niveaux" className="hover:text-white">Sécurité</a>
          <a href="#mission" className="hover:text-white">À propos</a>
        </div>
      </div>
    </footer>
  );
}
