import "server-only";
import type { Source, SourceHit } from "@/lib/types";
import type { ModelProvider } from "./types";
// 모델 호출이 없습니다. 정해진 규칙으로 같은 도구 흐름을 재현합니다.
export const demoProvider: ModelProvider = {
  mode: "demo",
  async decide({ domain, messages, toolResults }) {
    const latest = messages.at(-1)?.content ?? "";
    const priorQuestion =
      messages.filter((t) => t.role === "user").at(-2)?.content ?? "";
    const waiting =
      messages.at(-2)?.role === "assistant" &&
      messages.at(-2)?.content.includes("어떤 직무");
    const query = waiting ? `${priorQuestion} ${latest}` : latest;
    if (!toolResults.length) {
      if (
        domain === "data" &&
        /추천|매칭|골라|찾아/.test(latest) &&
        !/python|파이썬|rag|llm|ml|머신|데이터|sql|spark|airflow/i.test(query)
      )
        return {
          type: "answer",
          text: "어떤 직무와 기술 스택을 기준으로 매칭할까요? 예: ML 엔지니어(PyTorch·RAG) 또는 데이터 엔지니어(SQL·Spark). 그 외 분야는 준비된 공고에 없습니다.",
          sourceIds: [],
        };
      return {
        type: "tool_call",
        callId: "demo-search",
        name: "search_sources",
        arguments: { query },
      };
    }
    const last = toolResults.at(-1)!;
    if (!last.ok)
      return {
        type: "answer",
        text: "공고를 확인하는 중 문제가 발생했습니다. 확인하지 못한 내용을 답하지 않겠습니다. 잠시 후 다시 시도해주세요.",
        sourceIds: [],
      };
    const search = toolResults.find((t) => t.request.name === "search_sources");
    const hits = (search?.value ?? []) as SourceHit[];
    if (!hits.length)
      return {
        type: "answer",
        text: "이 조건에 맞는 검토된 공고가 아직 없습니다. 현재 자료로는 매칭을 제공하기 어렵습니다. 다른 기술 스택으로 다시 검색하거나 공식 채용 페이지를 확인해주세요.",
        sourceIds: [],
      };
    const read = toolResults.find((t) => t.request.name === "read_source");
    if (!read)
      return {
        type: "tool_call",
        callId: "demo-read",
        name: "read_source",
        arguments: { id: hits[0].id },
      };
    const source = read.value as Source;
    if (/연봉|급여|처우|보상/.test(latest))
      return {
        type: "answer",
        text: `${source.title} 공고는 찾았지만, 준비된 요약에는 연봉·처우 정보가 없습니다. 이 자료만으로 연봉을 단정할 수 없습니다. 원문 공고와 담당자에게 확인해야 합니다.`,
        sourceIds: [source.id],
      };
    if (domain === "data" && waiting)
      return {
        type: "answer",
        text: `${source.body}\n\n말씀하신 직무·기술 기준으로 이 공고를 읽은 매칭 데모입니다. 실제 매칭 점수와 강점·보완점은 모델 연결 후 이력서를 분석해 계산합니다. 지원 전 원문 공고와 마감일을 확인하세요.`,
        sourceIds: [source.id],
      };
    return {
      type: "answer",
      text: `${source.body}\n\n준비된 공고를 읽어 요건을 보여주는 데모입니다. 이력서와의 강점·보완점은 규칙 기반 예시이며, 지원 전 원문 공고와 마감일을 확인하세요.`,
      sourceIds: [source.id],
    };
  },
};
