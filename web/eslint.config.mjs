import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

const eslintConfig = [
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    // 생성물 — 직접 수정/린트 대상 아님
    ignores: [
      "node_modules/**",
      ".next/**",
      "components/ui/**",
      "lib/api-types/**", // openapi-typescript 생성물 (#41)
      "hooks/use-mobile.ts",
      "resume-match-agent-main/**",
    ],
  },
];

export default eslintConfig;
