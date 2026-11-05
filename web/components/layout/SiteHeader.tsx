import Link from "next/link";
import { FileSearch } from "lucide-react";
import { SITE_NAME } from "@/constants/site";

export const SiteHeader = () => {
  return (
    <header className="border-b border-slate-200/70 bg-white/80">
      <div className="page-shell flex min-h-20 flex-wrap items-center justify-between gap-3 py-4">
        <Link
          href="/"
          className="flex items-center gap-3"
          aria-label={`${SITE_NAME} 홈`}
        >
          <span className="flex size-10 items-center justify-center rounded-2xl bg-slate-900 text-white">
            <FileSearch size={23} />
          </span>
          <span className="text-sm font-semibold tracking-tight">
            {SITE_NAME}
          </span>
        </Link>
        <nav
          aria-label="주 메뉴"
          className="flex items-center gap-5 text-sm text-slate-600"
        >
          <Link href="/backend" className="hover:text-blue-600">
            백엔드·서버
          </Link>
          <Link href="/data" className="hover:text-blue-600">
            데이터·AI
          </Link>
        </nav>
      </div>
    </header>
  );
};
