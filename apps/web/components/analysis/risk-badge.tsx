import { RISK_LABELS, type RiskLevel } from "@safeclick/shared";
import { cn } from "@/lib/utils";

const styles: Record<RiskLevel, string> = {
  low: "border-safe-500/30 bg-safe-500/10 text-green-300",
  medium: "border-warn-500/30 bg-warn-500/10 text-amber-300",
  high: "border-danger-500/30 bg-danger-500/10 text-red-300",
};

export function RiskBadge({ level }: { level: RiskLevel }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold",
        styles[level],
      )}
    >
      {RISK_LABELS[level]}
    </span>
  );
}
