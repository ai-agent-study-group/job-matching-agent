import Link from "next/link";
import {
  ArrowRight,
  Server,
  Database,
  FolderSearch,
  BookOpen,
  MessageCircle,
  ArrowUpRight,
  FileText,
  CheckCircle2,
  AlertCircle,
  Link2,
} from "lucide-react";
export default function Home() {
  return (
    <main id="main" className="page-shell py-12 sm:py-20">
      <section className="grid items-center gap-12 lg:grid-cols-[1.15fr_1fr]">
        <div>
          <p className="eyebrow mb-5">RESUME MATCHING</p>
          <h1 className="text-4xl font-semibold leading-[1.25] tracking-tight sm:text-5xl">
            반복되는 구직,
            <br />
            공고를 찾아 이력서와 맞추는
            <br />
            <span className="text-blue-600">에이전트와 함께.</span>
          </h1>
          <p className="mt-6 max-w-md text-base leading-8 text-slate-500">
            채용공고를 찾아 이력서와 비교하고, 강점과 보완할 점을 확인하세요.
            관련 공고의 요건과 원문 출처를 함께 안내합니다.
          </p>
          <Link
            href="/backend"
            className="mt-7 inline-flex items-center gap-2 rounded-full bg-slate-900 px-6 py-3 text-sm font-medium text-white"
          >
            매칭 시작하기 <ArrowRight size={16} />
          </Link>
          <p className="mt-4 text-xs text-slate-500">
            현재는 AI API 없이 실행하는 학습용 데모입니다.
          </p>
        </div>
        <div className="relative rounded-[2rem] bg-[#edf2f7] p-6 sm:p-9">
          <div className="flex items-center gap-2 text-xs font-medium text-slate-600">
            <span className="size-2 rounded-full bg-blue-500" />
            조건에서 근거 있는 매칭까지
          </div>
          <div className="ml-8 mt-7 rounded-2xl rounded-tr-sm bg-blue-600 p-5 text-sm text-white shadow-lg shadow-blue-900/10">
            Java/Spring 경험으로 지원할 공고가 있나요?
          </div>
          <div className="mt-4 rounded-2xl bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center gap-2 text-xs text-slate-500">
              <FolderSearch size={16} />
              채용공고에서 관련 요건 확인
            </div>
            <p className="text-sm leading-7">
              조건에 맞는 공고를 찾고,
              <br />
              요건과 출처를 함께 확인합니다.
            </p>
            <div className="mt-5 rounded-xl bg-slate-50 px-4 py-3 text-xs text-slate-500">
              검색 → 읽기 → 매칭
            </div>
          </div>
          <p className="mt-5 text-center text-xs text-slate-600">
            개념을 설명하기 위한 예시 화면
          </p>
        </div>
      </section>
      <section className="mt-20">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <p className="eyebrow mb-3">CHOOSE YOUR FIELD</p>
            <h2 className="section-title">어떤 직무를 찾고 있나요?</h2>
          </div>
          <span className="hidden text-xs text-slate-500 sm:block">
            직무별 공고부터 비교해보세요
          </span>
        </div>
        <div className="grid gap-5 md:grid-cols-2">
          {[
            {
              path: "backend",
              name: "백엔드·서버",
              icon: Server,
              description: "서버 개발 공고의 요건과 이력서를 비교해보세요.",
              color: "bg-blue-50 text-blue-600",
              example: "Java · Node · 트래픽",
            },
            {
              path: "data",
              name: "데이터·AI",
              icon: Database,
              description: "데이터·ML 공고와 역량 차이를 살펴보세요.",
              color: "bg-emerald-50 text-emerald-600",
              example: "Python · RAG · 파이프라인",
            },
          ].map((item) => (
            <Link
              key={item.path}
              href={`/${item.path}`}
              className="soft-card group p-7 transition hover:-translate-y-1 hover:border-blue-200"
            >
              <div className="flex justify-between">
                <span
                  className={`flex size-12 items-center justify-center rounded-2xl ${item.color}`}
                >
                  <item.icon size={24} />
                </span>
                <ArrowUpRight
                  className="text-slate-300 transition group-hover:text-blue-600"
                  size={22}
                />
              </div>
              <h3 className="mt-6 text-xl font-semibold">{item.name}</h3>
              <p className="mt-3 text-sm leading-7 text-slate-500">
                {item.description}
              </p>
              <p className="mt-5 text-xs font-medium text-slate-500">
                {item.example}
              </p>
            </Link>
          ))}
        </div>
      </section>
      <section className="mt-20">
        <div className="mb-6">
          <p className="eyebrow mb-3">EXAMPLE MATCH</p>
          <h2 className="section-title">매칭 결과는 이렇게 보입니다</h2>
          <p className="mt-3 max-w-xl text-sm leading-7 text-slate-500">
            이력서와 채용공고를 비교한 예시입니다. 아래는 설명을 위한 데모
            데이터이며, 실제 점수·강점·보완점은 모델 연결 후 계산합니다.
          </p>
        </div>
        <div className="grid gap-5 lg:grid-cols-[300px_1fr]">
          <div className="soft-card p-6">
            <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
              <FileText size={16} />
              이력서 요약 (예시)
            </div>
            <p className="mt-4 text-sm font-semibold">백엔드 엔지니어 · 4년</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {["Java", "Spring Boot", "REST API", "MySQL", "Docker"].map(
                (s) => (
                  <span
                    key={s}
                    className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-600"
                  >
                    {s}
                  </span>
                ),
              )}
            </div>
          </div>
          <div className="soft-card p-7">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-medium text-slate-500">
                  매칭된 공고
                </p>
                <h3 className="mt-1 text-lg font-semibold">
                  핀테크 스타트업 — 백엔드 엔지니어
                </h3>
              </div>
              <div className="shrink-0 text-right">
                <p className="text-3xl font-semibold text-blue-600">82%</p>
                <p className="text-xs text-slate-400">요건 적합도</p>
              </div>
            </div>
            <div className="mt-6 grid gap-5 sm:grid-cols-2">
              <div>
                <p className="mb-3 flex items-center gap-2 text-xs font-semibold text-emerald-600">
                  <CheckCircle2 size={15} />
                  강점 — 요건 충족
                </p>
                <ul className="space-y-2 text-sm leading-6 text-slate-600">
                  <li>· Java·Spring Boot 서버 개발 (필수 3년↑ 충족)</li>
                  <li>· REST API 설계 경험</li>
                  <li>· 관계형 데이터베이스(MySQL) 경험</li>
                </ul>
              </div>
              <div>
                <p className="mb-3 flex items-center gap-2 text-xs font-semibold text-amber-600">
                  <AlertCircle size={15} />
                  보완 — 우대 사항
                </p>
                <ul className="space-y-2 text-sm leading-6 text-slate-600">
                  <li>· Kubernetes·AWS 운영 경험 미기재</li>
                  <li>· MSA 구조 경험 보강 필요</li>
                  <li>· 결제·정산 도메인 이해 강조 권장</li>
                </ul>
              </div>
            </div>
            <div className="mt-6 flex items-center gap-2 border-t border-slate-100 pt-4 text-xs text-slate-500">
              <Link2 size={14} />
              출처: 사람이 검토한 채용공고 요약 ·{" "}
              <code className="text-slate-400">backend-fintech</code>
            </div>
          </div>
        </div>
      </section>
      <section className="mt-16 rounded-3xl bg-slate-900 px-7 py-9 text-white sm:px-10">
        <h2 className="text-xl font-semibold">매칭은 이렇게 진행됩니다</h2>
        <div className="mt-7 grid gap-6 sm:grid-cols-3">
          {[
            [
              FolderSearch,
              "01",
              "조건 전달",
              "원하는 직무와 보유 기술을 적어주세요.",
            ],
            [
              BookOpen,
              "02",
              "검색과 읽기",
              "조건에 맞는 공고를 찾아 요건을 읽습니다.",
            ],
            [
              MessageCircle,
              "03",
              "매칭과 출처",
              "강점·보완점과 공고 출처를 함께 확인하세요.",
            ],
          ].map(([Icon, num, title, text]) => {
            const I = Icon as typeof FolderSearch;
            return (
              <div key={String(num)}>
                <I size={22} className="mb-4 text-blue-300" />
                <p className="text-sm font-semibold">
                  <span className="mr-2 text-slate-400">{String(num)}</span>
                  {String(title)}
                </p>
                <p className="mt-2 text-sm leading-7 text-slate-400">
                  {String(text)}
                </p>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}
