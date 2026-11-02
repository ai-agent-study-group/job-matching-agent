import type { Activity, ChatResult, Domain, Source, SourceHit, Turn } from "./types";
import { searchSources, readSource } from "./search";

// 규칙 기반 목(mock) 에이전트. 실제 모델 호출이 없다.
// 실제 백엔드가 붙으면 runAgent를 /api 호출로 교체하고, 아래 decide 규칙은 모델이 대신한다.

const MAX_CALLS = 3;

type Decision =
  | { type: "answer"; text: string; sourceIds: string[] }
  | { type: "search"; query: string }
  | { type: "read"; id: string };

interface State {
  searched: boolean;
  hits: SourceHit[];
  source: Source | null; // 마지막으로 읽은 공고
}

/** demo.ts의 규칙을 그대로 옮긴 결정 함수 — 검색→읽기→답변 순서를 재현한다. */
const decide = (domain: Domain, messages: Turn[], state: State): Decision => {
  const latest = messages.at(-1)?.content ?? "";
  const priorQuestion =
    messages.filter((t) => t.role === "user").at(-2)?.content ?? "";
  const waiting =
    messages.at(-2)?.role === "assistant" &&
    (messages.at(-2)?.content.includes("어떤 직무") ?? false);
  const query = waiting ? `${priorQuestion} ${latest}` : latest;

  if (!state.searched) {
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
    return { type: "search", query };
  }

  if (!state.hits.length)
    return {
      type: "answer",
      text: "이 조건에 맞는 검토된 공고가 아직 없습니다. 현재 자료로는 매칭을 제공하기 어렵습니다. 다른 기술 스택으로 다시 검색하거나 공식 채용 페이지를 확인해주세요.",
      sourceIds: [],
    };

  if (!state.source) return { type: "read", id: state.hits[0].id };

  const source = state.source;
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
};

/** 검색·읽기 도구를 돌려 매칭 답변과 활동 기록·출처를 만든다. async는 백엔드 교체를 위한 자리. */
export const runAgent = async (
  domain: Domain,
  messages: Turn[],
): Promise<ChatResult> => {
  const activities: Activity[] = [];
  const read = new Map<string, Source>();
  const state: State = { searched: false, hits: [], source: null };

  const finish = (answer: string, ids: string[]): ChatResult => ({
    answer,
    citations: [...new Set(ids)].flatMap((id) => {
      const s = read.get(id);
      return s
        ? [{ id: s.id, title: s.title, url: s.url, reviewedAt: s.reviewedAt, kind: s.kind }]
        : [];
    }),
    activities,
  });

  for (let count = 0; count <= MAX_CALLS; count++) {
    const decision = decide(domain, messages, state);

    if (decision.type === "answer") {
      activities.push({
        type: "answer",
        label: "답변 완료",
        detail: "데모 규칙으로 답변을 구성했습니다. 실제 AI 호출은 없습니다.",
      });
      return finish(decision.text, decision.sourceIds);
    }

    if (count === MAX_CALLS) {
      activities.push({
        type: "limit",
        label: "도구 호출 종료",
        detail: `도구는 질문당 ${MAX_CALLS}회까지만 실행합니다.`,
      });
      return finish(
        "도구 호출 한도에 도달했습니다. 질문을 좁혀 다시 시도해주세요.",
        [],
      );
    }

    if (decision.type === "search") {
      state.hits = searchSources(domain, decision.query);
      state.searched = true;
      activities.push({
        type: "search",
        label: "자료 검색",
        detail: `검색어: ${decision.query} · 관련 자료 ${state.hits.length}개`,
      });
    } else {
      const s = readSource(domain, decision.id);
      if (s) {
        read.set(s.id, s);
        state.source = s;
        activities.push({ type: "read", label: "자료 읽기", detail: s.title });
      }
    }
  }

  return finish("실행을 종료했습니다.", []);
};
