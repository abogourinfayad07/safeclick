"use client";

const labels: Record<string, string> = {
  low: "Risque faible",
  medium: "Risque moyen",
  high: "Risque élevé",
  unverified: "Non vérifié",
  confirmed: "Confirmé",
  dismissed: "Écarté",
};

export function StatsBars({ values }: { values: Record<string, number> }) {
  const entries = Object.entries(values);
  const max = Math.max(1, ...entries.map(([, value]) => value));

  return (
    <div className="mt-4 space-y-3">
      {entries.map(([key, value]) => (
        <div key={key} className="flex items-center gap-3">
          <span className="w-32 shrink-0 text-xs text-slate-400">
            {labels[key] ?? key}
          </span>
          <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/10">
            <div
              className="h-full rounded-full bg-electric-500"
              style={{ width: `${(value / max) * 100}%` }}
            />
          </div>
          <span className="w-8 text-right text-xs text-white">{value}</span>
        </div>
      ))}
    </div>
  );
}
