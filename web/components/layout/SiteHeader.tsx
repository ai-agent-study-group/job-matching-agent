import Link from "next/link";
import { BriefcaseBusiness, FileSearch, House, UserRound } from "lucide-react";
import { SITE_NAME } from "@/constants/site";
import { NavLink } from "./NavLink";

export const SiteHeader = () => {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-card">
      <div className="page-shell flex h-14 items-center justify-between gap-3">
        <Link
          href="/"
          className="flex items-center gap-2"
          aria-label={`${SITE_NAME} 홈`}
        >
          <span className="flex size-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <FileSearch size={20} />
          </span>
          <span className="hidden text-sm font-semibold tracking-tight sm:inline">
            {SITE_NAME}
          </span>
        </Link>
        <nav aria-label="주 메뉴" className="flex items-center">
          <NavLink
            href="/"
            icon={<House className="size-5" aria-hidden />}
            label="홈"
          />
          <NavLink
            href="/profile"
            icon={<UserRound className="size-5" aria-hidden />}
            label="내 프로필"
          />
          <NavLink
            href="/matches"
            icon={<BriefcaseBusiness className="size-5" aria-hidden />}
            label="매칭 결과"
          />
        </nav>
      </div>
    </header>
  );
};
