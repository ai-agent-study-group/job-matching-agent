import type { Domain } from "@/lib/types";
export const domains = {
  backend: {
    title: "백엔드·서버",
    subtitle: "서버 개발 공고와 내 이력서를 맞춰볼 때",
    description:
      "백엔드·서버 개발 공고를 검토된 자료에서 찾아 요건과 이력서를 비교해보세요.",
    label: "백엔드 매칭",
    examples: [
      "Java/Spring 경험으로 지원할 공고가 있나요?",
      "대용량 트래픽 서버 공고의 요건을 알려주세요",
      "이 공고에서 제 이력서에 부족한 기술은?",
    ],
    instruction:
      "백엔드·서버 개발 채용공고의 요건을 한국어로 안내하고, 이력서와의 강점·보완점을 설명한다. 읽은 공고만 근거로 사용하며, 자료가 없는 공고는 확인 불가를 설명한다. 합격 여부나 연봉을 단정하지 않는다.",
  },
  data: {
    title: "데이터·AI",
    subtitle: "데이터·ML 공고와 역량을 맞춰볼 때",
    description:
      "데이터·AI 엔지니어 공고를 공식 자료와 함께 확인하고 역량 차이를 살펴보세요.",
    label: "데이터·AI 매칭",
    examples: [
      "ML 엔지니어 공고를 추천해주세요",
      "RAG/LLM 경험이 필요한 공고가 있나요?",
      "데이터 파이프라인 공고의 필수 요건은?",
    ],
    instruction:
      "데이터·AI 엔지니어 채용공고의 요건을 한국어로 안내하고 이력서와의 매칭을 설명한다. 어떤 직무·기술을 기준으로 매칭할지 불분명하면 먼저 묻는다. 읽은 공고를 근거로 설명하며 합격 가능성이나 개별 지원 결과를 확정하지 않는다.",
  },
} satisfies Record<
  Domain,
  {
    title: string;
    subtitle: string;
    description: string;
    label: string;
    examples: string[];
    instruction: string;
  }
>;
export function isDomain(value: unknown): value is Domain {
  return value === "backend" || value === "data";
}
