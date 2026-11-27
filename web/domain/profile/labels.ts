import type { components } from "@/lib/api-types/api.generated";

export type Profile = components["schemas"]["Profile-Output"];

const SENIORITY: Record<string, string> = {
  intern: "인턴",
  junior: "주니어",
  mid: "미드",
  senior: "시니어",
  lead: "리드",
};

const LANGUAGE_LEVEL: Record<string, string> = {
  basic: "기초",
  good: "능숙",
  fluent: "유창",
  native: "원어민",
};

// ISO 639-1. 표에 없는 코드는 그대로 보여 줌
const LANGUAGE: Record<string, string> = {
  de: "독일어",
  en: "영어",
  ko: "한국어",
  fr: "프랑스어",
  es: "스페인어",
  it: "이탈리아어",
  ja: "일본어",
  zh: "중국어",
};

export const seniorityLabel = (code: string | null) =>
  code ? (SENIORITY[code] ?? code) : "알 수 없음";

export const languageLabel = (code: string) => LANGUAGE[code] ?? code;

export const languageLevelLabel = (level: string | null) =>
  level ? (LANGUAGE_LEVEL[level] ?? level) : "수준 미기재";

// "2023-01" → "2023.01", "2020" → "2020", 그 밖의 글은 그대로
export const formatDate = (value: string) =>
  value.replace(
    /^(\d{4})-(\d{1,2})$/,
    (_, y, m) => `${y}.${m.padStart(2, "0")}`,
  );

export const formatPeriod = (
  start: string | null,
  end: string | null,
  ongoing = "재직 중",
) => `${start ? formatDate(start) : "?"} – ${end ? formatDate(end) : ongoing}`;

export const formatMonths = (months: number) => {
  const years = Math.floor(months / 12);
  const rest = months % 12;
  if (years === 0) return `${rest}개월`;
  return rest === 0 ? `${years}년` : `${years}년 ${rest}개월`;
};
