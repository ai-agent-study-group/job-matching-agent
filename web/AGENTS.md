# AGENTS.md

Codex 및 기타 코딩 에이전트용 안내. 이 폴더(`web/`)는 job-matching-agent의 프론트엔드(Next.js JMA 앱)다. **전체 가이드는 [CLAUDE.md](CLAUDE.md)가 단일 출처 — 작업 전 읽는다.** 아래는 빠른 참조다.

## 스택

Next.js 16 (App Router) · React 19 · TypeScript(strict) · Tailwind v4 · shadcn/ui(Radix) · lucide-react · **Zustand**(클라 상태) · **TanStack Query**(서버 데이터, `components/shared/Providers.tsx`) · npm. 애니메이션은 CSS 우선. **i18n 미사용**(단일 언어, `lang="ko"`). Cloudflare·테스트 러너는 미도입.

## 명령어

```bash
npm install          # .npmrc legacy-peer-deps 적용
npm run dev          # :3000
npm run build
npm run lint         # eslint
npm run type-check   # tsc --noEmit
```

## 꼭 지킬 것

- **규칙 정본은 레포 루트 [`docs/fe/`](../docs/fe/)** (web 폴더 아님) — [TECH.md](../docs/fe/TECH.md)(구조·스택) · [AI_RULES.md](../docs/fe/AI_RULES.md)(서버/클라·선언 스타일) · [ANIMATION.md](../docs/fe/ANIMATION.md) · [FEATURE.md](../docs/fe/FEATURE.md) · [web-app.md](../docs/fe/web-app.md)(개요).
- **구조**: 목적별 레이어. `app·components → domain → data·constants → utils·lib`. 역방향 import 금지. 별칭 `@/*` → `web/` 루트.
- **컴포넌트**: 라우트 진입점만 `export default function`, 나머지는 `const` 화살표 함수. 기본 Server Component, 필요 시만 `'use client'`. `any` 금지.
- **`components/ui/`는 shadcn 생성물** — 직접 수정 금지, 바깥 래퍼로 커스터마이즈.
- **shadcn add 함정**: `npx shadcn@latest add` 후 `cn` import가 깨짐 → `sed -i '' 's|from "cn"|from "@/utils/style"|g' components/ui/*.tsx`.
- **Tailwind**: 기본 스케일 우선, 임의 값 `[]` 금지. 토큰은 `app/globals.css`.
- **브랜치/PR**: `main`에서 `<type>/<설명>` 분기, 코드 변경은 PR + CI 통과. 루트 [CONTRIBUTING.md](../CONTRIBUTING.md).

자세한 내용은 [CLAUDE.md](CLAUDE.md).
