import { SourceCollectionGuide } from "@/components/source-collection-guide";
import Link from "next/link";
import { ArrowRight, Code2, Users, Check, Search, Target, Send } from "lucide-react";
export const metadata = {
  title: "내부 구현 가이드",
  robots: { index: false, follow: false },
};
const pipeline = [
  {
    icon: Search,
    step: "01",
    title: "수집 에이전트",
    role: "채용 사이트·공고 메일을 모니터링해 신규 공고를 정형 데이터(JSON)로 가져옵니다.",
    now: "Python 수집 스크립트와 검토 대기 파일. 기본 앱은 사람이 정리한 공고 요약을 사용합니다.",
    file: "scripts/scrape/ · data/pending/",
  },
  {
    icon: Target,
    step: "02",
    title: "매칭·평가 에이전트",
    role: "이력서와 공고를 비교해 일치도를 계산하고 부족한 역량(Gap)을 찾습니다.",
    now: "검색·읽기 도구로 공고를 찾아 요건을 보여주는 규칙 기반 데모. 점수 계산은 모델 연결 후 구현합니다.",
    file: "lib/tools/sources.ts · lib/agents/run.ts",
  },
  {
    icon: Send,
    step: "03",
    title: "리포트·액션 에이전트",
    role: "매칭 결과를 정리해 리포트를 만들고, 맞춤 자기소개서 초안 등 지원을 돕습니다.",
    now: "답변에 공고 요건과 출처를 함께 반환. 알림·자소서 생성은 이후 확장 대상입니다.",
    file: "lib/providers/ · app/api/chat/route.ts",
  },
];
const weeks = [
  {
    num: "01",
    title: "AI와 대화하기",
    goal: "질문과 담당 역할을 전달하면 매칭 설명이 어떻게 바뀔까요?",
    dev: "모델 연결 자리를 살펴보고, 선택한 AI의 어댑터를 연결합니다.",
    everyone: "같은 조건을 다른 역할 설명으로 실행하고 매칭 설명을 비교합니다.",
    file: "lib/providers/ · lib/agents/domains.ts",
  },
  {
    num: "02",
    title: "공고를 찾아 읽기",
    goal: "AI에게 공고 요건을 주면 매칭이 어떻게 달라질까요?",
    dev: "Python 수집 예제를 실행하고 검색·읽기 함수를 수정합니다.",
    everyone:
      "원문 공고와 수집 결과를 비교하고, 검색에 필요한 기술 스택 키워드를 추가합니다.",
    file: "scripts/scrape/ · lib/tools/sources.ts",
  },
  {
    num: "03",
    title: "도구를 쓰는 에이전트",
    goal: "언제 공고를 검색하고, 언제 사용자에게 조건을 되물어야 할까요?",
    dev: "실제 모델의 도구 요청을 실행 루프에 연결합니다.",
    everyone: "활동 기록을 보고 도구 선택과 추가 질문이 적절한지 확인합니다.",
    file: "lib/agents/run.ts · lib/providers/types.ts",
  },
  {
    num: "04",
    title: "실패를 찾아 개선하기",
    goal: "매칭이 잘못됐을 때 어느 부분을 고쳐야 할까요?",
    dev: "검색·맥락·실행 오류를 구분해 수정하고 재검증합니다.",
    everyone: "백엔드·데이터 팀이 서로 테스트하고 수정 전후 결과를 발표합니다.",
    file: "docs/EVALUATION.md · tests/",
  },
];
export default function Admin() {
  return (
    <main id="main" className="page-shell py-12 sm:py-16">
      <section className="max-w-2xl">
        <p className="eyebrow mb-4">INTERNAL GUIDE · ADMIN</p>
        <h1 className="text-4xl font-semibold leading-tight tracking-tight">
          페이지별 구현 가이드와
          <br />
          스터디 실습 안내.
        </h1>
        <p className="mt-5 text-base leading-8 text-slate-500">
          웹은 준비되어 있습니다. 조건을 보내는 것부터 공고를 찾아 읽고 이력서와
          매칭하는 에이전트까지, 동작을 관찰하며 직접 만들어봅니다.
        </p>
      </section>
      <p className="mt-6 rounded-xl bg-slate-100 p-4 text-sm leading-7 text-slate-600">
        스터디원용 내부 안내입니다. 공개 메뉴에는 연결하지 않습니다. 현재 로그인
        보호는 없으므로 주소를 아는 사람은 열 수 있습니다. 공개 배포 전 관리자
        인증을 구현해야 합니다.
      </p>
      <section className="mt-10 space-y-4" aria-labelledby="pipeline-title">
        <div>
          <p className="eyebrow mb-3">AGENT PIPELINE</p>
          <h2 id="pipeline-title" className="section-title">
            세 단계 에이전트 파이프라인
          </h2>
          <p className="mt-4 text-sm leading-7 text-slate-600">
            수집 → 매칭·평가 → 리포트·액션의 3단계로 설계합니다. 현재 데모는 이
            흐름을 규칙 기반으로 재현하며, 각 단계를 실제 모델·수집·알림으로
            확장합니다.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {pipeline.map((p) => (
            <article key={p.step} className="soft-card p-6">
              <span className="flex size-10 items-center justify-center rounded-2xl bg-blue-50 text-blue-600">
                <p.icon size={20} />
              </span>
              <p className="eyebrow mt-4 text-blue-600">STEP {p.step}</p>
              <h3 className="mt-2 text-lg font-semibold">{p.title}</h3>
              <p className="mt-3 text-sm leading-7 text-slate-600">{p.role}</p>
              <p className="mt-3 text-xs leading-6 text-slate-500">
                현재: {p.now}
              </p>
              <p className="mt-4 break-words rounded-xl bg-slate-50 p-3 font-mono text-xs leading-6 text-slate-600">
                {p.file}
              </p>
            </article>
          ))}
        </div>
      </section>
      <SourceCollectionGuide />
      <section
        className="mt-10 space-y-4"
        aria-labelledby="implementation-title"
      >
        <h2 id="implementation-title" className="section-title">
          각 페이지는 어떻게 만들까요?
        </h2>
        {[
          {
            route: "/",
            title: "홈 · 직무 선택",
            files: "app/page.tsx · components/site-header.tsx",
            now: "서비스 소개와 두 직무 분야로 가는 버튼을 표시합니다.",
            steps: [
              "사용자가 찾는 직무 분야를 고르게 합니다.",
              "소개·예시 조건·출처 확인 방법을 정리합니다.",
              "공개 메뉴는 백엔드·서버와 데이터·AI만 유지합니다.",
            ],
          },
          {
            route: "/backend",
            title: "백엔드·서버 매칭",
            files:
              "app/backend/page.tsx · components/domain-page.tsx · components/chat-panel.tsx",
            now: "공통 채팅 화면에 backend 분야와 예시 조건을 전달합니다.",
            steps: [
              "data/backend.json에 검토한 공고와 기술 스택 키워드를 추가합니다.",
              "lib/agents/domains.ts에서 매칭 설명 범위와 되물어야 할 조건을 작성합니다.",
              "기술 스택이 부족한 조건·요건 근거·공고 없는 조건을 비교합니다.",
            ],
          },
          {
            route: "/data",
            title: "데이터·AI 매칭",
            files: "app/data/page.tsx · lib/agents/domains.ts · data/data.json",
            now: "백엔드 페이지와 같은 화면을 사용하되 대화와 공고를 별도로 다룹니다.",
            steps: [
              "ML·데이터 공고를 검토하고 data/data.json에 등록합니다.",
              "직무·기술 기준이 필요한 때 추가 질문 규칙을 작성합니다.",
              "모호한 추천 요청 뒤 직무를 답했을 때 맥락과 출처를 확인합니다.",
            ],
          },
          {
            route: "/api/chat",
            title: "매칭이 만들어지는 서버",
            files: "app/api/chat/route.ts · lib/agents/run.ts · lib/providers/",
            now: "입력을 검증하고 데모 제공자가 검색·읽기 도구를 실행합니다.",
            steps: [
              "모델을 선택하고 ModelProvider 인터페이스에 맞는 연결 코드를 작성합니다.",
              "모델의 도구 요청을 실행하고 결과를 다시 모델에 전달합니다.",
              "실제 AI 모드 표시·시간 제한·사용량 제한을 연결합니다.",
            ],
          },
          {
            route: "공고 준비",
            title: "Python 수집과 검토",
            files:
              "scripts/scrape/ · data/pending/ · lib/sources/repository.ts",
            now: "채용 페이지를 검토 대기 파일로 수집하고 사람이 승인한 공고만 읽습니다.",
            steps: [
              "수집 URL과 본문 위치를 sources.json에 지정합니다.",
              "원문 공고와 수집 결과를 비교하고 기술 키워드를 보완합니다.",
              "review.py로 승인한 뒤 채팅의 검색 결과를 확인합니다.",
            ],
          },
          {
            route: "/admin",
            title: "내부 안내 페이지",
            files: "app/admin/page.tsx · README.md · docs/STUDY.md",
            now: "페이지별 구현 안내와 4주 학습 과정을 모아 직접 주소로 접근합니다.",
            steps: [
              "스터디 질문과 구현 방법을 업데이트합니다.",
              "공개 배포 전 서버에서 관리자 로그인과 권한을 확인합니다.",
              "추후 공고 검토 기능을 붙일 때 쓰기 API도 관리자 권한으로 보호합니다.",
            ],
          },
        ].map((item) => (
          <article key={item.route} className="soft-card p-6">
            <p className="eyebrow text-blue-600">{item.route}</p>
            <h3 className="mt-2 text-lg font-semibold">{item.title}</h3>
            <p className="mt-3 text-sm leading-7 text-slate-600">
              현재: {item.now}
            </p>
            <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm leading-7 text-slate-600">
              {item.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
            <p className="mt-4 break-words rounded-xl bg-slate-50 p-3 font-mono text-xs leading-6 text-slate-600">
              수정 위치: {item.files}
            </p>
          </article>
        ))}
      </section>
      <h2 className="section-title mt-14">4주 실습 순서</h2>
      <section className="mt-10 grid gap-4 sm:grid-cols-3">
        {[
          ["LLM 연결", "조건을 보내고 매칭 설명을 받습니다."],
          ["공고 기반 매칭", "코드가 공고를 찾아 모델에 전달합니다."],
          [
            "도구 사용 에이전트",
            "모델이 필요한 도구와 다음 행동을 선택합니다.",
          ],
        ].map(([title, text], i) => (
          <div className="soft-card p-6" key={title}>
            <p className="eyebrow text-blue-600">STEP {i + 1}</p>
            <h2 className="mt-3 font-semibold">{title}</h2>
            <p className="mt-3 text-sm leading-7 text-slate-500">{text}</p>
          </div>
        ))}
      </section>
      <p className="mt-5 rounded-xl bg-amber-50 px-5 py-4 text-sm leading-7 text-amber-900">
        현재 웹은 도구 흐름을 보여주는 규칙 기반 데모입니다. 실제 모델을 연결한
        뒤 ‘모델이 행동을 선택하는 과정’을 실습합니다.
      </p>
      <section className="mt-14 space-y-5">
        {weeks.map((w) => (
          <article
            className="soft-card grid gap-6 p-6 sm:p-8 md:grid-cols-[180px_1fr]"
            key={w.num}
          >
            <div>
              <p className="eyebrow text-blue-600">WEEK {w.num}</p>
              <h2 className="mt-3 text-xl font-semibold">{w.title}</h2>
            </div>
            <div>
              <p className="text-sm font-medium leading-7">{w.goal}</p>
              <div className="mt-4 space-y-3 text-sm leading-7 text-slate-500">
                <p className="flex gap-3">
                  <Code2 size={17} className="mt-1 shrink-0" />
                  {w.dev}
                </p>
                <p className="flex gap-3">
                  <Users size={17} className="mt-1 shrink-0" />
                  {w.everyone}
                </p>
              </div>
              <p className="mt-5 break-words rounded-xl bg-slate-50 px-4 py-3 font-mono text-xs text-slate-500">
                실습 위치: {w.file}
              </p>
            </div>
          </article>
        ))}
      </section>
      <section className="mt-12 grid gap-8 rounded-3xl bg-slate-900 p-8 text-white sm:grid-cols-2">
        <div>
          <h2 className="text-xl font-semibold">개발 경험이 없어도 괜찮아요</h2>
          <p className="mt-4 text-sm leading-8 text-slate-400">
            실제 구직 조건을 만들고, 공고 원문을 확인하고, 매칭 규칙을 고쳐보세요.
            개발 경험자와 짝을 이루어 실행과 설정 변경도 직접 해봅니다.
          </p>
        </div>
        <div>
          <h2 className="text-xl font-semibold">마지막에 보여줄 세 가지</h2>
          <ul className="mt-4 space-y-3 text-sm text-slate-300">
            {[
              "공고를 찾고 출처와 함께 매칭 설명하기",
              "조건이 부족하면 직무·기술 추가 질문하기",
              "맞는 공고가 없으면 확인 불가 안내하기",
            ].map((t) => (
              <li className="flex items-center gap-2" key={t}>
                <Check size={16} className="text-blue-300" />
                {t}
              </li>
            ))}
          </ul>
        </div>
      </section>
      <div className="mt-8 flex flex-wrap items-center justify-between gap-4 text-sm text-slate-500">
        <p>주 1회 · 2시간 · 조건 3개를 비교하는 작은 과제</p>
        <Link
          href="/backend"
          className="flex items-center gap-2 font-medium text-blue-600"
        >
          데모부터 살펴보기
          <ArrowRight size={16} />
        </Link>
      </div>
    </main>
  );
}
