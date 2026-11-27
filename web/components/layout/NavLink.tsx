"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Route } from "next";
import type { ReactNode } from "react";
import { cn } from "@/utils/style";

/** 아이콘 위 · 글자 아래 메뉴. 지금 페이지면 밑줄 */
export const NavLink = ({
  href,
  icon,
  label,
}: {
  href: Route;
  /** 렌더한 아이콘. 서버 컴포넌트가 아이콘 컴포넌트 자체는 넘길 수 없음 */
  icon: ReactNode;
  label: string;
}) => {
  const pathname = usePathname();
  const active = href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <Link
      href={href}
      aria-current={active ? "page" : undefined}
      className={cn(
        "flex h-14 min-w-16 flex-col items-center justify-center gap-0.5 border-b-2 px-2 text-xs transition-colors",
        active
          ? "border-foreground text-foreground"
          : "border-transparent text-muted-foreground hover:text-foreground",
      )}
    >
      {icon}
      <span className="sr-only sm:not-sr-only">{label}</span>
    </Link>
  );
};
