export function PageHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <section className="border-b border-white/10">
      <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{title}</h1>
        <p className="mt-3 max-w-3xl text-sm leading-relaxed text-slate-300">{subtitle}</p>
      </div>
    </section>
  );
}
