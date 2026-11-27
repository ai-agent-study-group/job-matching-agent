import type { components } from "@/lib/api-types/api.generated";
import { throwIfFailed } from "./error";

type Profile = components["schemas"]["Profile-Output"];
export type JobPosting = components["schemas"]["JobPosting"];

/** 프로필에 맞는 공고를 찾음. /api/profile 응답을 그대로 보내도 됨 (BE가 계산 필드를 버림) */
export const postSearch = async (profile: Profile): Promise<JobPosting[]> => {
  const res = await fetch("/api/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  await throwIfFailed(res);
  return res.json();
};
