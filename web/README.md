# web

사이트 목록 설정, 이력 직접 등록, 공고별 평가 결과와 매칭 근거 확인을 위한 프론트엔드(JMA 앱)입니다.

이력서 업로드·파싱과 대화 보충 화면은 추후 범위입니다. PoC의 이력 입력 형식, API 계약과 화면 연결은 [10월 20일 안건](../docs/meetings/2026-10-20.md)에서 정합니다.

## 기술 스택

- **Next.js 16** (App Router) · **React 19** · **TypeScript** (strict)
- **Tailwind CSS v4** + **shadcn/ui** (new-york, Radix 기반) · **lucide-react**
- 상태: **Zustand**(클라이언트) · **TanStack Query**(서버 데이터 — `components/shared/Providers.tsx`로 주입)
- 패키지 매니저 **npm** (`.npmrc`에 `legacy-peer-deps=true` — shadcn peer 충돌 회피)

**i18n은 사용하지 않습니다** — 단일 언어(한국어), `<html lang="ko">` 고정.

계획(필요 시 도입): 애니메이션은 CSS 우선, 복잡할 때만 Framer Motion. 로컬 저장 `idb`/`localforage`. 테스트 `Vitest`/`Playwright`. Cloudflare는 현재 미사용. 근거는 [docs/fe/TECH.md](../docs/fe/TECH.md).

## 실행

```bash
cd web
npm install
npm run dev          # http://localhost:3000
```

| 명령 | 내용 |
| --- | --- |
| `npm run dev` | 개발 서버 |
| `npm run build` | 프로덕션 빌드 |
| `npm run start` | 빌드 실행 |
| `npm run lint` | ESLint |
| `npm run type-check` | `tsc --noEmit` |
| `npm run format` | Prettier (docs/·skills/·components/ui/ 제외) |

## 구조

목적별 레이어(Purpose-first) 구조입니다. 의존은 위→아래만 흐릅니다(역방향 import 금지).

```
app·components  →  domain  →  data·constants  →  utils·lib
```

- import 별칭 `@/*` → `web/` 루트.
- `components/` — `ui/`(shadcn 생성물) · `layout/`(전역 네비) · `shared/`(2개+ 도메인 재사용) · `<도메인>/`.
- `components/ui/`는 shadcn 생성물 — 직접 수정하지 않고 바깥 래퍼로 커스터마이즈.
- 라우트 진입점(`app/**/page.tsx`·`layout.tsx`)만 `export default function`, 나머지 컴포넌트는 `const` 화살표 함수.
- 색인 대상 콘텐츠는 서버 컴포넌트, 인터랙션만 `'use client'`.

## 규칙·설계 문서 (레포 루트 `docs/fe/`)

규칙의 단일 출처는 **레포 루트 [`docs/fe/`](../docs/fe/)** 입니다(web 폴더가 아닙니다). 코드 작성 전 읽으세요:

- [TECH.md](../docs/fe/TECH.md) — 스택·폴더 구조·상태관리·SEO·네이밍
- [AI_RULES.md](../docs/fe/AI_RULES.md) — 서버/클라 컴포넌트·선언 스타일·Tailwind 우선순위
- [ANIMATION.md](../docs/fe/ANIMATION.md) — 애니메이션 용어·CSS 구현
- [FEATURE.md](../docs/fe/FEATURE.md) — 공통 기능 패턴 (설정·공유·예외 처리)
- [web-app.md](../docs/fe/web-app.md) — web 앱 구성 개요

에이전트용 요약은 [CLAUDE.md](CLAUDE.md) · [AGENTS.md](AGENTS.md).

### shadcn 컴포넌트 추가

커스텀 `utils` 별칭(`@/utils/style`) 때문에 `npx shadcn@latest add <comp>` 후 `cn` import가 깨집니다. 추가 후 수정하세요:

```bash
sed -i '' 's|from "cn"|from "@/utils/style"|g' components/ui/*.tsx
```
