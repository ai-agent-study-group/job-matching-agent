# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

이 폴더(`web/`)는 job-matching-agent의 프론트엔드(JMA 앱)다. 문서는 한국어가 기본이며 코드 식별자·명령어는 원문 그대로 둔다. (백엔드·문서 도구는 레포 루트에서 별도 `uv`/npm으로 관리한다.)

## 기술 스택

Next.js 16 (App Router) · React 19 · TypeScript(strict) · Tailwind CSS v4 · shadcn/ui(new-york, Radix) · lucide-react. 패키지 매니저 **npm**.

상태: **Zustand**(클라이언트 상태) · **TanStack Query**(서버 데이터 캐싱, `components/shared/Providers.tsx`가 루트 레이아웃에 주입). 애니메이션은 **CSS 우선**, spring·drag·enter/exit처럼 CSS로 안 되는 것만 Framer Motion 검토(ANIMATION.md). **i18n은 쓰지 않는다** — 단일 언어(한국어), `<html lang="ko">` 고정. `[lang]` 세그먼트·Dictionary·hreflang·next-intl 없음. 로컬 저장(`idb`/`localforage`)·테스트(Vitest/Playwright)·Cloudflare는 **현재 미도입**(필요 시 docs 기준으로 추가).

## 명령어

```bash
npm install          # .npmrc의 legacy-peer-deps=true 적용 (shadcn peer 충돌 회피)
npm run dev          # http://localhost:3000
npm run build
npm run lint         # eslint
npm run type-check   # tsc --noEmit
npm run format       # prettier --write (docs/·skills/·components/ui/ 제외)
```

테스트 러너는 아직 없다(Vitest/Playwright 미설정).

## 규칙의 단일 출처 — 레포 루트 `docs/fe/`

FE 규칙의 정본은 **레포 루트의 [`docs/fe/`](../docs/fe/)** 에 있다(web 폴더가 아니다). 코드 작성 전 읽는다. **CLAUDE.md는 요약이고, 아래가 정본이다.**

- [TECH.md](../docs/fe/TECH.md) — 기술 스택, 목적별 레이어 폴더 구조, 상태관리, SEO, 네이밍, 성능.
- [AI_RULES.md](../docs/fe/AI_RULES.md) — 서버/클라이언트 컴포넌트 구분, 컴포넌트 선언 스타일, Tailwind 우선순위, 응답 규칙.
- [ANIMATION.md](../docs/fe/ANIMATION.md) — 애니메이션 용어 15개와 CSS 구현(요청 시 용어로 지정).
- [FEATURE.md](../docs/fe/FEATURE.md) — 공통 기능 패턴(설정 화면·공유·예외 처리 등).
- [web-app.md](../docs/fe/web-app.md) — web 앱 구성 개요(스택·구조·실행).

`skills/`에는 shadcn·next-coding-rules·next-seo 등 세부 규칙 스킬이 있다.

## 아키텍처 (목적별 레이어 / Purpose-first)

코드를 **무엇을 하는가**로 나눠 루트의 목적별 폴더에 둔다. `src/` 래퍼·`features/` 격리를 쓰지 않는다. import 별칭 `@/*` → `web/` 루트. 의존은 위→아래만, 역방향 import 금지.

```
app·components  →  domain  →  data·constants  →  utils·lib
(페이지·UI)        (앱 고유 로직)  (데이터·설정값)      (순수 유틸·외부 연동)
```

- `app/` — App Router 페이지·레이아웃·route handler·sitemap·robots.
- `components/` — `ui/`(shadcn 생성물) · `layout/`(전역 네비) · `shared/`(2개+ 도메인 재사용) · `<도메인>/`. 콜로케이션(`_components`) 금지, 중앙 집중.
- `domain/` — 계산·매칭·검증 등 이 앱 고유 로직. UI import 금지, 순수 함수 지향.
- `constants/` — 변하지 않는 설정값(`site.ts`의 `SITE_URL` 등). 하드코딩 금지, 여기서만.
- `utils/` — 순수 유틸(`style.ts`의 `cn` 등). `lib/` — 외부 SDK·인프라 어댑터만.

### 컴포넌트 작성 규칙 (핵심)

- 라우트 진입점(`app/**/page.tsx`·`layout.tsx`·`error.tsx`)만 `export default function`, 나머지 컴포넌트는 전부 `const` 화살표 함수.
- 기본 **Server Component**, 사용자 입력·브라우저 API 필요할 때만 `'use client'`. 색인 대상 콘텐츠는 서버 렌더(SEO).
- `components/ui/`는 shadcn 생성물 — **직접 수정 금지**. 커스터마이즈는 `ui/` 밖 래퍼로.
- Tailwind는 기본 스케일 우선, 임의 값 `[]` 하드코딩 금지. 브랜드 값만 `globals.css` 토큰으로(`bg-accent-yellow` 등).
- `any` 금지.

## 스타일 토큰

`app/globals.css`가 단일 출처다. 디자인 팔레트를 shadcn 시맨틱 토큰(`--background`·`--primary`…) + 브랜드 액센트 + 라이트/다크 블록으로 구현한다. 색·radius 변경은 여기 한 곳에서.

## shadcn 컴포넌트 추가

`components.json`의 `aliases.utils`는 `@/lib/utils`이고, `web/lib/utils.ts`가 cn 본체(`utils/style.ts`)를 재노출하는 shim이다. TECH.md 규칙(cn 본체는 `utils/style.ts`)을 지키면서 shadcn이 `import { cn } from "@/lib/utils"`로 정상 생성되게 한다. 과거엔 utils 별칭이 `@/utils/style`이라 add 시 `import { cn } from "cn"`로 깨지고 가짜 `cn` npm 패키지가 설치돼 매번 sed·uninstall이 필요했는데, shim으로 해결됨.

shadcn이 생성한 `hooks/use-mobile.ts`는 next의 strict 룰에 걸려 `eslint.config.mjs`의 ignore에 들어있다(생성물이라 수정 안 함).

## 브랜치 / PR

`main`에서 `<type>/<짧은-설명>`로 분기(`feat`·`fix`·`refactor`·`test`·`docs`·`chore`). 코드·화면·설정 변경은 PR + 승인 1명 + CI 통과 필수. 레포 루트 [CONTRIBUTING.md](../CONTRIBUTING.md) 참고.
