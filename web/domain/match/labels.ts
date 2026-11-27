import type { Check } from "@/lib/api/match";

export const VERDICT: Record<Check["verdict"], string> = {
  met: "충족",
  partial: "부분 충족",
  unmet: "미충족",
  unknown: "확인 불가",
};

// 화면에 보이는 순서도 이 순서
export const KIND: Record<Check["kind"], string> = {
  requirement: "필수 요건",
  nice_to_have: "우대 사항",
  responsibility: "담당 업무",
  skill: "기술",
  qualification: "자격",
  condition: "근무 조건",
};

export const formatScore = (score: number) => `${Math.round(score * 100)}%`;

/** kind 순서대로 묶음. 빈 묶음은 뺌 */
export const groupByKind = (checks: Check[]) =>
  (Object.keys(KIND) as Check["kind"][])
    .map((kind) => ({ kind, checks: checks.filter((c) => c.kind === kind) }))
    .filter((g) => g.checks.length > 0);

export const countMet = (checks: Check[]) =>
  checks.filter((c) => c.verdict === "met").length;
