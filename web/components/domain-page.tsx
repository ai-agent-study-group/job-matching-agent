import Link from "next/link";
import { ArrowLeft, FlaskConical, FolderOpen } from "lucide-react";
import { ChatPanel } from "./chat-panel";
import { domains } from "@/lib/agents/domains";
import type { Domain } from "@/lib/types";
export function DomainPage({ domain }: { domain: Domain }) {
  const c = domains[domain];
  return (
    <main id="main" className="page-shell py-9 sm:py-12">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-xs text-slate-500"
      >
        <ArrowLeft size={13} />
        주제 선택으로
      </Link>
      <div className="mt-7 mb-8">
        <p className="eyebrow mb-3">
          {domain === "backend" ? "BACKEND & SERVER" : "DATA & AI"}
        </p>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
          {c.title} 매칭
        </h1>
        <p className="mt-3 text-sm leading-7 text-slate-500">{c.description}</p>
      </div>
      <p className="mb-5 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-xs leading-6 text-amber-900">
        학습용 데모 · 실제 AI 미연결 — 정해진 규칙으로 로컬 자료를 검색하고
        읽습니다.
      </p>
      <div className="grid items-start gap-6 lg:grid-cols-[1fr_280px]">
        <ChatPanel key={domain} domain={domain} />
        <aside className="space-y-4">
          <section className="rounded-2xl border border-amber-200 bg-amber-50/70 p-5">
            <FlaskConical className="text-amber-600" size={20} />
            <h2 className="mt-3 text-sm font-semibold">학습용 데모입니다</h2>
            <p className="mt-2 text-xs leading-6 text-slate-600">
              실제 AI 모델은 연결되지 않았습니다. 정해진 규칙으로 검색·읽기를
              실행하고 준비된 설명을 보여줍니다.
            </p>
          </section>
          <section className="soft-card p-5">
            <FolderOpen size={20} className="text-slate-400" />
            <h2 className="mt-3 text-sm font-semibold">지금 읽는 공고</h2>
            <p className="mt-2 text-xs leading-6 text-slate-500">
              사람이 확인한 채용공고의 짧은 요약입니다. 실시간 검색이 아니며,
              모든 조건에 맞는 공고가 준비되어 있지는 않습니다.
            </p>
            <p className="mt-3 text-xs leading-6 text-slate-500">
              일반 정보 안내입니다. 개인의 합격 가능성이나 연봉을 판단하지
              않습니다.
            </p>
          </section>
        </aside>
      </div>
    </main>
  );
}
