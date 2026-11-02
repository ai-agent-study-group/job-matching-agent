import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

const eslintConfig = [
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    // shadcn 생성물 — 직접 수정/린트 대상 아님
    ignores: [
      "node_modules/**",
      ".next/**",
      "components/ui/**",
      "hooks/use-mobile.ts",
      "resume-match-agent-main/**",
    ],
  },
];

export default eslintConfig;
