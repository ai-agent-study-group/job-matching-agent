import sources from "@/scripts/scrape/sources.json";
import { ExternalLink } from "lucide-react";

const notes: Record<
  string,
  { purpose: string; section: string; question: string }
> = {
  "wwr-backend": {
    purpose: "백엔드 공고 목록",
    section:
      "카테고리 페이지의 공고 목록(section.jobs 안의 각 항목). 제목·회사·태그를 추출합니다.",
    question: "원격 백엔드 공고에는 어떤 기술이 요구되나요?",
  },
  "wwr-devops": {
    purpose: "DevOps·인프라 공고 목록",
    section:
      "카테고리 페이지의 공고 목록. 데이터·인프라 직무의 제목과 태그를 살펴봅니다.",
    question: "인프라·파이프라인 공고는 어떤 요건을 요구하나요?",
  },
};
const sample = {
  id: sources[0].id,
  domain: sources[0].domain,
  title: sources[0].title,
  url: sources[0].url,
  keywords: sources[0].keywords.slice(0, 3),
  language: "en",
  body: "여기에 공고 페이지에서 추출한 본문이 저장됩니다.",
  collectedAt: "<실제 수집 시각: UTC>",
  reviewed: false,
  reviewedAt: "",
  kind: "scraped",
};
export function SourceCollectionGuide() {
  return (
    <section
      id="collection-examples"
      aria-labelledby="collection-title"
      className="mt-10 space-y-5"
    >
      <div>
        <p className="eyebrow mb-3">DATA COLLECTION EXAMPLES</p>
        <h2 id="collection-title" className="section-title">
          어느 채용 사이트에서 무엇을 가져오나요?
        </h2>
        <p className="mt-4 text-sm leading-7 text-slate-600">
          아래 링크로 실제 채용 사이트를 열어보세요. Python은 페이지를
          다운로드하고 공고 목록 본문만 골라 파일로 저장합니다. 사이트마다 HTML
          구조가 다르고 수집을 제한할 수 있으니 robots.txt와 이용약관을 먼저
          확인합니다.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {sources.map((source) => {
          const note = notes[source.id] ?? {
            purpose: "추가 공고",
            section:
              "수집 목록에 지정한 본문 위치를 확인하고 필요한 공고를 검토합니다.",
            question: "이 공고로 답할 수 있는 조건을 팀에서 작성해보세요.",
          };
          return (
            <article key={source.id} className="soft-card p-6">
              <p className="eyebrow text-blue-600">
                {source.domain === "backend" ? "백엔드·서버" : "데이터·AI"} ·{" "}
                {note.purpose}
              </p>
              <h3 className="mt-3 text-lg font-semibold">{source.title}</h3>
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 inline-flex items-center gap-2 text-sm font-medium text-blue-700"
              >
                채용 페이지 열기
                <ExternalLink size={14} />
              </a>
              <p className="mt-2 break-all text-xs leading-6 text-slate-600">
                {source.url}
              </p>
              <dl className="mt-4 space-y-3 text-sm leading-7">
                <div>
                  <dt className="font-medium">가져올 부분</dt>
                  <dd className="text-slate-600">{note.section}</dd>
                </div>
                <div>
                  <dt className="font-medium">연결할 조건 예시</dt>
                  <dd className="text-slate-600">{note.question}</dd>
                </div>
                <div>
                  <dt className="font-medium">저장할 파일</dt>
                  <dd className="break-all font-mono text-xs text-slate-600">
                    data/pending/{source.id}.json
                  </dd>
                </div>
              </dl>
              <details className="mt-4 border-t border-slate-100 pt-3">
                <summary className="cursor-pointer text-xs font-medium text-slate-600">
                  개발자용: 본문 위치와 설정
                </summary>
                <p className="mt-3 text-xs leading-6 text-slate-600">
                  본문 위치(selector)는 <code>{source.selector}</code>입니다.
                  페이지 안에서 공고 목록에 붙은 이름을 이용해 해당 부분만
                  선택합니다. 수집 대상은 scripts/scrape/sources.json에서
                  지정합니다.
                </p>
              </details>
            </article>
          );
        })}
      </div>
      <article className="soft-card p-6">
        <h3 className="text-lg font-semibold">
          첫 실습: 백엔드 공고 목록 한 개부터
        </h3>
        <ol className="mt-4 list-decimal space-y-3 pl-5 text-sm leading-7 text-slate-600">
          <li>
            위의 백엔드 공고 링크를 열고 공고 목록이 어떻게 구성되는지 봅니다.
          </li>
          <li>Python 가상환경과 의존성을 준비한 뒤 아래 명령을 실행합니다.</li>
          <li>data/pending/wwr-backend.json을 열고 원문과 비교합니다.</li>
          <li>
            중복·광고·불필요한 항목이 없는지 확인하고, 필요하면 한국어 요약과
            기술 키워드를 보완합니다.
          </li>
          <li>
            사람이 검토를 마친 뒤 승인 명령을 실행합니다. 이후 백엔드 매칭에서
            검색·출처를 확인합니다.
          </li>
        </ol>
        <pre
          tabIndex={0}
          role="region"
          aria-label="한 페이지 수집과 승인 명령"
          className="mt-4 overflow-x-auto rounded-xl bg-slate-900 p-4 text-xs leading-7 text-slate-100"
        >
          <code>
            {
              "# 1. 백엔드 공고 목록 한 건 수집\npython3 scripts/scrape/collect.py --manifest scripts/scrape/backend-example.json\n\n# 2. 생성 파일을 직접 검토한 뒤에만 승인\npython3 scripts/scrape/review.py --approve wwr-backend"
            }
          </code>
        </pre>
        <p className="mt-3 text-xs leading-6 text-slate-600">
          명령은 개발자가 프로젝트 폴더에서 실행합니다. 비개발자는 원문과 파일을
          비교하고 검색 키워드를 제안합니다. 승인하면 같은 ID의 기존 앱 공고가
          교체됩니다.
        </p>
      </article>
      <article className="soft-card p-6">
        <h3 className="text-lg font-semibold">
          수집 후 파일은 이렇게 생깁니다
        </h3>
        <p className="mt-3 text-sm leading-7 text-slate-600">
          아래는 구조를 설명하는 예시입니다. 실제 파일에는 공고 본문과 실제 수집
          시각이 들어갑니다. 아직 검토하지 않았으므로 reviewed는 false이고,
          매칭에서 읽지 않습니다.
        </p>
        <pre
          tabIndex={0}
          role="region"
          aria-label="수집 결과 JSON 예시"
          className="mt-4 overflow-x-auto rounded-xl bg-slate-50 p-4 text-xs leading-6 text-slate-700"
        >
          <code>{JSON.stringify(sample, null, 2)}</code>
        </pre>
        <p className="mt-4 text-sm leading-7 text-slate-600">
          채용 페이지 → Python 수집 → 검토 대기 파일 → 사람의 검토·승인 →
          data/backend.json 또는 data/data.json → 매칭의 검색·읽기 도구
        </p>
        <p className="mt-3 text-xs leading-6 text-slate-600">
          기본 앱의 공고는 사람이 정리한 요약이고, 위 수집 예제는 채용 사이트
          목록입니다. 수집했다고 자동으로 앱 공고에 추가되지는 않습니다.
        </p>
      </article>
      <p className="rounded-xl bg-amber-50 p-4 text-sm leading-7 text-amber-900">
        링크드인 등 대부분의 채용 플랫폼은 자동 수집을 차단하거나 약관으로
        금지하며, 공식 API 사용을 권장합니다. 우회하지 않고 기본 실습은 수집을
        허용하는 공개 공고 사이트로 진행합니다. 차단 동작을 관찰하려면
        `scripts/scrape/linkedin-example.json` 매니페스트로 수집을 시도해보세요.
      </p>
    </section>
  );
}
