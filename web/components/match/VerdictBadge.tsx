import { CheckCircle2, CircleDashed, CircleHelp, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { VERDICT } from "@/domain/match/labels";
import type { Check } from "@/lib/api/match";
import { cn } from "@/utils/style";

const STYLE: Record<
  Check["verdict"],
  { icon: typeof CheckCircle2; className: string }
> = {
  met: { icon: CheckCircle2, className: "bg-emerald-50 text-emerald-700" },
  partial: { icon: CircleDashed, className: "bg-amber-50 text-amber-700" },
  unmet: { icon: XCircle, className: "bg-red-50 text-red-700" },
  unknown: { icon: CircleHelp, className: "bg-slate-100 text-slate-600" },
};

export const VerdictBadge = ({ verdict }: { verdict: Check["verdict"] }) => {
  const { icon: Icon, className } = STYLE[verdict];
  return (
    <Badge className={cn("shrink-0 gap-1 rounded-full", className)}>
      <Icon aria-hidden />
      {VERDICT[verdict]}
    </Badge>
  );
};
