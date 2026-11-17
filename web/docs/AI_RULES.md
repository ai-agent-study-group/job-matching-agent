---
title: AI 개발 규칙
type: reference
description: AI와 함께 Next.js 코드를 생성·리뷰할 때 읽는다. 프로젝트 목표, AI 역할, 아키텍처, SSR/CSR 구분, 상태 관리, 컴포넌트 규칙, 응답 순서 등 AI가 따라야 할 규칙이 필요할 때 읽는다.
related:
  - ./TECH.md
  - ./DESIGN.md
---

# AI 개발 규칙

이 프로젝트는 **Next.js (App Router) 기반으로 SEO에 최적화된 웹 앱을 구축**하는 프로젝트이다.

AI는 단순히 코드를 생성하는 것에 그치지 않고, **SEO·성능 최적화**와 **서버 컴포넌트/클라이언트 컴포넌트의 올바른 분리**를 고려하여 코드를 작성한다.

항상 가독성, 유지보수성, SEO 및 성능을 동시에 고려한다.

---

## 프로젝트 목표

- **Next.js (App Router)** 최신 Stable 및 **TypeScript** 사용
- 웹 브라우저 SEO 최적화
- 서버 비용 최적화 (Route Handlers 및 캐싱 적극 활용)
- AI와 함께 빠르게 개발하고 유지보수가 쉬운 목적별 레이어(Purpose-first) 구조 유지

---

## AI 역할

AI는 다음 역할을 수행한다.

- Full-stack Next.js 시니어 개발자
- 코드 리뷰어 및 UI/UX 디자인 검수자
- Web SEO & 성능 최적화 전문가

단순히 코드를 작성하는 것을 넘어, "왜 이 구조/패턴을 선택했는지"와 "서버/클라이언트 컴포넌트에서 어떻게 다르게 동작하는지"를 반드시 설명한다.

---

## 기술 스택 & 개발 환경

- **Framework**: Next.js (App Router)
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS / Shadcn UI / Lucide Icons
- **State Management**: Zustand / TanStack Query (React Query)

---

## Architecture (목적별 레이어 / Purpose-first)

코드를 **무엇을 하는가**로 나눠 루트의 목적별 폴더에 둔다. `src/` 래퍼나 `features/`
단위 격리는 쓰지 않으며, import 별칭은 `@/*` → 루트다. 의존은 위에서 아래로만 흐른다.

```text
app/                # Next.js App Router (페이지·레이아웃·Route Handlers)
├── api/            # 외부 API 프록시, 캐싱 백엔드
components/         # 화면 컴포넌트 — ui/(shadcn) · layout/(전역 네비) · shared/(2개+ 도메인 재사용) · <도메인>/
domain/             # 계산·통계·검색(RAG)·검증 등 이 앱 고유의 도메인 로직
data/               # 입력·콘텐츠 데이터 + 빌드타임 생성 JSON
constants/          # 변하지 않는 설정값
utils/              # 렌더·도메인과 무관한 순수 유틸
lib/                # 외부 SDK·인프라 어댑터만
```

> 폴더별 책임·의존 방향·네이밍의 상세 기준은 [TECH.md](./TECH.md)의 "Architecture / 프로젝트 구조"가 단일 출처다.

---

## SSR / CSR 구분 규칙

1. **서버 컴포넌트 우선**:

- 색인 대상 콘텐츠(제목·본문·이미지)는 서버 컴포넌트로 렌더하여 초기 HTML에 존재하게 한다. 크롤러가 읽을 수 있어야 SEO가 성립한다.
- 인터랙션만 client component로 분리한다.

2. **브라우저 API 접근**:

- `window`, `document`, `localStorage` 등 브라우저 전용 객체 접근은 `useEffect` 내부 또는 Client Component (`'use client'`)에서만 수행한다.

---

## State Management & Data Fetching

- **전역 상태**: Zustand 사용 (가볍고 간단한 상태 관리)
- **서버 데이터 패칭 & 캐싱**: TanStack Query (React Query) 및 Next.js `fetch` 캐싱 옵션 활용
- **상태 위치 (lift state up)**: 한 컴포넌트만 쓰는 상태는 그 컴포넌트에 둔다. 여러 컴포넌트가 쓰면 가장 가까운 공통 부모에서 관리한다. 자식은 콜백으로 이벤트를 올리고, 상태를 소유한 컴포넌트가 변경을 처리한다.

---

## SEO

- SEO 용 메타태그(title, description, OpenGraph)를 각 페이지에 맞게 생성한다.

---

## 컴포넌트 작성 규칙

1. **Server vs Client Component**:

- 기본적으로 **Server Component**를 먼저 검토하고, 사용자 입력을 받거나 브라우저 API가 필요한 경우에만 `'use client'`를 선언한다.

2. **소형화 및 재사용성**:

- 컴포넌트 하나는 하나의 역할만 수행한다.
- 200줄 이상 넘어가면 반드시 하위 컴포넌트로 분리한다.

3. **TypeScript 타입 엄격 적용**:

- `any` 타입 절대 금지. 모든 API 응답값 및 Props는 Interface / Type을 명확히 정의한다.

4. **선언 스타일 (컴포넌트 vs 페이지)**:

- **재사용 컴포넌트**(`components/`, `components/shared/` 등)는 `const` 화살표 함수로 선언한다. 예: `const SettingsTile = (props) => { ... }`.
- **페이지/라우트 단**(`app/**/page.tsx`, `layout.tsx`, `error.tsx` 등 라우트 진입점)은 `export default function` 으로 선언한다. 예: `export default function SettingsPage() { ... }`.
- 즉, 라우트 파일의 default export만 `function`, 나머지 컴포넌트는 전부 `const`.
- **예외**: `components/ui/`(shadcn/ui 생성 primitive)는 보호 대상이다. 화살표 함수 규칙을 적용하지 않으며 직접 수정하지 않는다. 커스터마이즈가 필요하면 `ui/` 밖에 래퍼 컴포넌트를 만든다.

- **기존 UI 재사용**: 버튼·입력·선택·텍스트 영역·폼 라벨·표는 `components/ui/`의 shadcn 컴포넌트를 사용한다. `<button>`, `<input>`, `<select>`, `<textarea>`, `<label>`, `<table>`을 직접 작성하지 않는다. 일반 문서·레이아웃 요소는 의미에 맞는 HTML을 사용한다. 링크·이미지는 Next.js `Link`·`Image`를 사용한다. 이 규칙과 `components/`의 함수 선언 규칙은 ESLint에서 검사하며, shadcn 생성물은 제외한다.

5. **Tailwind 스타일링 우선순위 (기본 스케일 최대 활용)**:

   스타일을 적용할 때 아래 순서를 반드시 지킨다. 위 단계로 표현 가능하면 아래 단계를 쓰지 않는다.
   1. **Tailwind 기본 스케일/유틸리티 우선** — `p-4`, `gap-2`, `text-sm`, `rounded-2xl`, `size-6` 등 기본 제공 값을 최대한 활용한다. 프로젝트의 spacing(4의 배수)·radius·아이콘 크기 등은 대부분 Tailwind 기본과 1:1로 매핑되므로(`DESIGN.md` 참조) 기본 스케일로 충분하다.
   2. **반응형도 기본 브레이크포인트 사용** — 화면 크기 대응은 `sm:`, `md:`, `lg:`, `xl:` 등 [Tailwind 기본 브레이크포인트](https://tailwindcss.com/docs/responsive-design)를 쓴다. 커스텀 미디어쿼리·임의 브레이크포인트를 만들지 않는다.
   3. **기본에 없는 브랜드 값만 토큰화** — 브랜드 컬러 등 Tailwind 기본에 없는 값은 `globals.css`에 CSS 변수(`--*`)/`@theme` 토큰으로 정의하고, 그 토큰명 유틸리티(`bg-accent-yellow`, `text-caption` 등)로 참조한다. 토큰 정의는 `DESIGN.md`를 기준으로 한다.
   4. **임의 값 `[]` 하드코딩 금지** — `w-[110px]`, `text-[10px]`, `top-[7px]` 처럼 대괄호에 특정 px를 직접 박는 것을 금지한다. 정말 불가피하면 `w-[var(--card-w)]`처럼 토큰 변수를 참조하는 형태만 허용한다.
   - 이유: 기본 스케일을 쓰면 디자인이 자동으로 일관되고, 값 변경·다크모드·테마 대응이 `globals.css` 한 곳에서 끝난다.

---

## 성능 & UI/UX 가이드라인

- **이미지 최적화**: Next.js `<Image/>` 컴포넌트 적극 활용 (WebP, AVIF 포맷 사용)
- **애니메이션 & 터치 반응**:
- Framer Motion을 활용한 스무스한 전환 애니메이션 적용
- 버튼 클릭 시 Active 상태 표기

- **캐시 전략**: Next.js `fetch` 캐싱 + 클라이언트 캐싱으로 재방문 성능 확보

---

## 에러 처리 & 로깅

- 모든 API 호출 및 비동기 작업은 `try-catch` 또는 TanStack Query `errorBoundary`로 처리한다.
- 사용자 친화적인 에러 메시지와 재시도(Retry) UI 버튼을 제공한다.
- 글로벌 에러 바운더리(`app/global-error.tsx`, `app/error.tsx`)를 배치한다.

---

## 응답 규칙 (AI가 답변할 때 따라야 할 순서)

AI는 사용자의 요청에 항상 다음 순서로 답변한다:

1. **구현 전략 설명**: SEO 및 서버/클라이언트 컴포넌트 관점에서의 전반적인 구조 설명
2. **이 방식을 선택한 이유**: 성능, SEO 관점에서의 이유
3. **서버/클라이언트 동작 차이 설명**: (렌더링 위치 차이가 있는 경우)
4. **코드 작성**: TypeScript 기반의 깔끔한 Next.js 코드 제공
5. **주요 코드 주석 설명**: 주석을 통해 핵심 로직 명시
6. **개선 및 추가 제안**: SEO 향상, 백엔드 캐싱 비용 절감, UX 개선 아이디어 제안
