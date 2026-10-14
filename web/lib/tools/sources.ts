import "server-only";
import type { Domain, Source, SourceHit } from "@/lib/types";
import {
  localRepository,
  type SourceRepository,
} from "@/lib/sources/repository";
const normalize = (s: string) => s.toLocaleLowerCase().normalize("NFKC");
export async function searchSources(
  domain: Domain,
  query: string,
  repository: SourceRepository = localRepository,
): Promise<SourceHit[]> {
  const text = normalize(query);
  const tokens = [
    ...new Set(text.split(/[^\p{L}\p{N}]+/u).filter((t) => t.length >= 2)),
  ];
  return (await repository.list(domain))
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
}
export async function readSource(
  domain: Domain,
  id: string,
  repository: SourceRepository = localRepository,
): Promise<Source | null> {
  return (
    (await repository.list(domain)).find(
      (s) => s.domain === domain && s.reviewed && s.id === id,
    ) ?? null
  );
}
export const toolDefinitions = [
  {
    name: "search_sources",
    description:
      "현재 직무 분야의 검토된 로컬 채용공고를 검색한다. 공고 본문은 별도 읽기 도구로 확인한다.",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string", maxLength: 500 } },
      required: ["query"],
      additionalProperties: false,
    },
  },
  {
    name: "read_source",
    description: "검색에서 얻은 공고 ID로 요건 본문과 출처를 읽는다.",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string" } },
      required: ["id"],
      additionalProperties: false,
    },
  },
] as const;
