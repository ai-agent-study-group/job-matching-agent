import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { SITE_DESCRIPTION, SITE_NAME, SITE_URL } from "@/constants/site";
import { Providers } from "@/components/shared/Providers";
import { SiteHeader } from "@/components/layout/SiteHeader";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: SITE_NAME,
    template: `%s · ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  openGraph: {
    type: "website",
    siteName: SITE_NAME,
    title: SITE_NAME,
    description: SITE_DESCRIPTION,
    url: SITE_URL,
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_NAME,
    description: SITE_DESCRIPTION,
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body className={`${inter.variable} font-sans antialiased`}>
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-white focus:p-4"
        >
          본문으로 건너뛰기
        </a>
        <SiteHeader />
        <Providers>{children}</Providers>
        <footer className="page-shell mt-16 flex flex-wrap justify-between gap-3 border-t border-slate-200 py-7 text-xs leading-6 text-slate-500">
          <span>{SITE_NAME} · 채용공고와 이력서를 한국어로 매칭.</span>
          <span>학습용 데모 · 실제 AI 미연결 · 일반 정보 안내</span>
        </footer>
      </body>
    </html>
  );
}
