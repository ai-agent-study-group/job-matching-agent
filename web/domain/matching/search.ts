import type { Domain, Source, SourceHit } from "./types";
import backendJobs from "@/data/jobs/backend.json";
import dataJobs from "@/data/jobs/data.json";

// 목데이터: 백엔드가 붙으면 이 두 import를 API 호출로 교체한다.
const JOBS: Record<Domain, Source[]> = {
  backend: backendJobs as unknown as Source[],
  data: dataJobs as unknown as Source[],
};

const normalize = (s: string) => s.toLocaleLowerCase().normalize("NFKC");

/** 검토된 로컬 공고를 키워드·본문 점수로 검색한다. */
export const searchSources = (domain: Domain, query: string): SourceHit[] => {
  const text = normalize(query);
  const tokens = [
    ...new Set(text.split(/[^\p{L}\p{N}]+/u).filter((t) => t.length >= 2)),
  ];
  return JOBS[domain]
    .filter((s) => s.domain === domain && s.reviewed)
    .map((s) => {
      const keywordScore = s.keywords.reduce(
        (n, k) => n + (text.includes(normalize(k)) ? 4 : 0),
        0,
      );
      const content = normalize(`${s.title} ${s.body}`);
      const score =
        keywordScore +
        tokens.reduce((n, t) => n + (content.includes(t) ? 1 : 0), 0);
      return { id: s.id, title: s.title, excerpt: s.body.slice(0, 160), score };
    })
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id))
    .slice(0, 3);
};

/** 검색 결과 ID로 공고 본문·출처를 읽는다. */
export const readSource = (domain: Domain, id: string): Source | null =>
  JOBS[domain].find((s) => s.domain === domain && s.reviewed && s.id === id) ??
  null;
