import type { Metadata } from "next";
import { SiteHeader } from "@/components/site-header";
import "./globals.css";
export const metadata: Metadata = {
  title: {
    default: "Resume Match Agent — 이력서 매칭 에이전트",
    template: "%s · Resume Match Agent",
  },
  description:
    "채용공고를 찾아 이력서와 비교하고, 강점·보완점과 출처를 함께 확인하세요.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-white focus:p-4"
        >
          본문으로 건너뛰기
        </a>
        <SiteHeader />
        {children}
        <footer className="page-shell mt-16 flex flex-wrap justify-between gap-3 border-t border-slate-200 py-7 text-xs leading-6 text-slate-500">
          <span>Resume Match Agent · 채용공고와 이력서를 한국어로 매칭.</span>
          <span>학습용 데모 · 실제 AI 미연결 · 일반 정보 안내</span>
        </footer>
      </body>
    </html>
  );
}
