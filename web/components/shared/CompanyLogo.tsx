import { Building2 } from "lucide-react";
import { cn } from "@/utils/style";

/** 회사 로고 자리. 로고 이미지가 없어 첫 글자를 씀. 회사가 없으면 건물 아이콘 */
export const CompanyLogo = ({
  name,
  className,
}: {
  name?: string | null;
  className?: string;
}) => (
  <span
    aria-hidden
    className={cn(
      "flex size-12 shrink-0 items-center justify-center rounded-md border border-border bg-slate-100 text-lg font-semibold text-slate-500",
      className,
    )}
  >
    {name?.trim()[0]?.toUpperCase() ?? <Building2 className="size-5" />}
  </span>
);
