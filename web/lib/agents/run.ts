import "server-only";
import type { Activity, ChatResult, Domain, Source, Turn } from "@/lib/types";
import { domains } from "./domains";
import { getProvider } from "@/lib/providers";
import type {
  ModelProvider,
  ToolRequest,
  ToolResult,
} from "@/lib/providers/types";
import {
  searchSources,
  readSource,
  toolDefinitions,
} from "@/lib/tools/sources";
import {
  localRepository,
  type SourceRepository,
} from "@/lib/sources/repository";
export async function runAgent(
  domain: Domain,
  messages: Turn[],
  options: {
    provider?: ModelProvider;
    repository?: SourceRepository;
    maxCalls?: number;
  } = {},
): Promise<ChatResult> {
  const provider = options.provider ?? getProvider();
  const repository = options.repository ?? localRepository;
  const maxCalls = options.maxCalls ?? 3;
  const activities: Activity[] = [];
  const toolResults: ToolResult[] = [];
  const read = new Map<string, Source>();
  const found = new Set<string>();
  const finish = (answer: string, ids: string[]): ChatResult => ({
    mode: "demo",
    answer,
    citations: [...new Set(ids)].flatMap((id) => {
      const s = read.get(id);
      return s
        ? [
            {
              id: s.id,
              title: s.title,
              url: s.url,
              reviewedAt: s.reviewedAt,
              kind: s.kind,
            },
          ]
        : [];
    }),
    activities,
  });
  for (let count = 0; count <= maxCalls; count++) {
    let decision;
    try {
      decision = await provider.decide({
        domain,
        instructions: domains[domain].instruction,
        messages,
        tools: toolDefinitions,
        toolResults,
      });
    } catch {
      activities.push({
        type: "error",
        label: "실행 오류",
        detail: "답변 제공자가 정상적으로 응답하지 않았습니다.",
      });
      return finish(
        "응답을 준비하지 못했습니다. 잠시 후 다시 시도해주세요.",
        [],
      );
    }
    if (decision.type === "answer") {
      activities.push({
        type: "answer",
        label: "답변 완료",
        detail: "데모 규칙으로 답변을 구성했습니다. 실제 AI 호출은 없습니다.",
      });
      return finish(decision.text, decision.sourceIds);
    }
    if (count === maxCalls) {
      activities.push({
        type: "limit",
        label: "도구 호출 종료",
        detail: `도구는 질문당 ${maxCalls}회까지만 실행합니다.`,
      });
      return finish(
        "도구 호출 한도에 도달했습니다. 질문을 좁혀 다시 시도해주세요.",
        [],
      );
    }
    const request: ToolRequest = decision;
    let result: ToolResult;
    try {
      if (
        !request.arguments ||
        typeof request.arguments !== "object" ||
        Array.isArray(request.arguments)
      )
        throw new Error("도구 입력은 객체여야 합니다.");
      const args = request.arguments as Record<string, unknown>;
      if (request.name === "search_sources") {
        if (
          Object.keys(args).length !== 1 ||
          typeof args.query !== "string" ||
          !args.query.trim() ||
          args.query.length > 500
        )
          throw new Error("검색어가 올바르지 않습니다.");
        const hits = await searchSources(domain, args.query, repository);
        hits.forEach((h) => found.add(h.id));
        activities.push({
          type: "search",
          label: "자료 검색",
          detail: `검색어: ${args.query} · 관련 자료 ${hits.length}개`,
        });
        result = { request, ok: true, value: hits };
      } else if (request.name === "read_source") {
        if (
          Object.keys(args).length !== 1 ||
          typeof args.id !== "string" ||
          !found.has(args.id)
        )
          throw new Error("검색 결과에 없는 자료는 읽을 수 없습니다.");
        const source = await readSource(domain, args.id, repository);
        if (!source) throw new Error("검토된 자료를 찾을 수 없습니다.");
        read.set(source.id, source);
        activities.push({
          type: "read",
          label: "자료 읽기",
          detail: source.title,
        });
        result = { request, ok: true, value: source };
      } else throw new Error("등록되지 않은 도구입니다.");
    } catch (error) {
      const detail =
        error instanceof Error ? error.message : "도구 실행에 실패했습니다.";
      activities.push({ type: "error", label: "도구 오류", detail });
      result = { request, ok: false, error: detail };
    }
    toolResults.push(result);
  }
  return finish("실행을 종료했습니다.", []);
}
