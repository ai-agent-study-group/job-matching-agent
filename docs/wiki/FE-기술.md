---
제목: "기술 스택 및 개발 규칙 (Next.js)"
유형: "위키"
설명: "GitHub Wiki 에서 자동 동기화된 문서입니다."
---

# 기술 스택 및 개발 규칙 (Next.js)

## 프로젝트 목표

이 프로젝트는 **Next.js (App Router)로 SEO에 최적화된 웹 앱**을 개발한다.

유지보수가 쉽고 AI와 함께 개발하기 좋은 구조를 목표로 하며, 서버 비용은 정적 export(SSG)·캐싱으로 최소화한다.

---

## 개발 환경

### Framework

Next.js (App Router, Latest Stable)

- 항상 Next.js Stable 버전을 사용한다.
- Experimental 기능은 사용하지 않는다.

---

### Language

TypeScript

- TypeScript 최신 Stable
- Strict Mode 필수 (`strict: true`)
- Type Alias / Utility Types 적극 활용
- 불변성(Immutability) 유지 및 `const` 사용 우선

---

## Architecture

### 목적별 레이어 (Purpose-first)

코드를 **무엇을 하는가**로 나눠 루트의 목적별 폴더에 둔다. 거대한 `lib/` 한 폴더에
전부 몰아넣지 않고, `core/` 같은 포괄 폴더도 쓰지 않는다. 각 폴더는 역할이 한 문장으로
설명돼야 하며, 역방향 의존(순수 유틸이 도메인 로직을 import)을 만들지 않는다.

의존 방향(위에서 아래로만):

```text
app/ (페이지·라우트)  ·  components/ (UI)
      ↓
domain/ (계산·통계·검색·검증 등 도메인 로직)
      ↓
data/ (입력·콘텐츠·생성 데이터)   constants/ (고정 설정값)
      ↓
utils/ (순수 유틸)   lib/ (외부 연동)
```

#### app / components (UI)

- `app/`: App Router 페이지·레이아웃·route handler·sitemap·robots.
- `components/`: 화면 컴포넌트. `components/ui/`는 shadcn 프리미티브(생성물)만.

#### domain (도메인 로직)

- 계산·집계, 검색(RAG), 입력 검증 등 **그 앱 고유의 규칙**.
- `data/`·`constants/`만 참조하고, UI를 import하지 않는다. 테스트하기 쉽게 순수 함수로.

#### data (데이터)

- 사람이 입력한 기준·콘텐츠 + 빌드타임에 생성한 데이터(JSON).
- 대용량 원본은 번들에 통째로 `import`하지 말고, 빌드타임 스크립트로 런타임에 실제 필요한
  slim 서브셋만 뽑아 그걸 `import`한다(배포 가이드 참고).

#### constants (고정 설정값)

- 도메인·문의 메일 등 **변하지 않는 값** 한 곳. 하드코딩 금지, 여기서만 관리.

#### utils (순수 유틸)

- 렌더링·도메인과 무관한 순수 함수(표시 형식, 공유, className 병합 등).

#### lib (외부 연동)

- 외부 SDK·인프라 어댑터(캡차, 스토리지 클라이언트 등)**만**. 도메인 로직을 넣지 않는다.

---

## 프로젝트 구조

코드를 목적별 루트 폴더로 나눈다. 아래는 재사용 가능한 기준 구조다(`<domain>`·`<route>`는
각 앱의 실제 이름으로 채운다). import 별칭은 `@/*` → 루트.

```text
app/                # Next.js App Router
├── api/            # Route Handlers (외부 API 프록시·검증·캐싱)
├── layout.tsx      # 루트 레이아웃 (공통 metadata, Provider)
├── page.tsx        # 홈 (서버 생성)
├── <route>/        # 라우트별 폴더 (page.tsx)
├── sitemap.ts      # 전 라우트 sitemap
├── robots.ts       # 크롤 정책
└── opengraph-image.*  # OG 대표 이미지

components/         # 화면 컴포넌트 — 도메인 폴더 단일 축
├── ui/             # shadcn 프리미티브 (생성물, 직접 수정 지양)
├── layout/         # 사이트 전역 레이아웃·네비 (헤더·푸터·로고 등)
├── shared/         # 2개+ 도메인에서 재사용하는 UI
└── <domain>/       # 도메인별 폴더

constants/          # 고정 설정값 (도메인·연락처 등 변하지 않는 값)
utils/              # 순수 유틸 (표시 형식·공유·className 병합 등)
data/               # 입력·콘텐츠 데이터 + 빌드타임 생성 JSON
domain/             # 도메인 로직 — 도메인/접두사별 폴더 + 단일 파일은 root
├── <domain>/       #   관련 모듈이 여러 개면 묶는다
└── *.ts            #   root: 그 외 단일 모듈
lib/                # 외부 연동만 (SDK·인프라 어댑터)

scripts/            # 데이터·빌드 파이프라인 — 단계별 폴더 (Node/tsx)
├── fetch/          #   외부 API 수집
├── build/          #   파생 데이터·에셋 생성
├── test/           #   파이프라인 검증 스크립트
├── lib/            #   스크립트 공용 유틸
└── *.mjs           #   root: 오케스트레이션 (refresh·validate 등)
public/             # 정적 에셋
app/globals.css     # 디자인 토큰 + 전역 스타일 (Tailwind v4)
```

### 폴더 한 줄 요약 — 다른 프로젝트에 복사해 갈 수 있나?

맨 위(UI)로 갈수록 "이 앱 전용", 맨 아래(utils)로 갈수록 "어느 앱에나 통용". **복사해 재사용하려면 아래쪽 폴더부터** 가져간다.

| 폴더          | 한 줄 요약                        | 복사 가능?                 | 예시                                                                      |
| ------------- | --------------------------------- | -------------------------- | ------------------------------------------------------------------------- |
| `app/`        | 라우트·페이지 (URL이 곧 폴더)     | ❌ 이 앱 전용              | `/calculator`, `/precedents/[id]`, `sitemap.ts`                           |
| `components/` | 화면에 어떻게 보일까 (UI)         | △ 디자인 시스템이면 재사용 | 버튼·모달·형량 결과 카드·조건 입력 폼                                     |
| `domain/`     | **이 서비스만의 규칙 (비즈니스)** | ❌ 오직 이 앱에서만 의미   | `sentencing.ts`: 초범 −3점·합의 −4점, 결과 0 이하면 벌금형                |
| `data/`       | 입력 콘텐츠 + 빌드 생성 JSON      | ❌ 이 앱 데이터            | `case-precedents.json`(판례 원본), `crimes.ts`                            |
| `constants/`  | 변하지 않는 설정값                | △ 값만 바꾸면 재사용       | 도메인 URL, 문의 메일                                                     |
| `lib/`        | 외부 기술·인프라 연동             | ✅ 설정만 맞추면 재사용    | `turnstile.ts`(캡차), `admin-auth.ts`, `usage-cache.ts`(D1)               |
| `utils/`      | 렌더링 돕는 일반 편의 도구        | ✅ 100% 어느 앱에서나      | `format.ts`(날짜 `2026.10.22`·천 단위 콤마), `style.ts`(`cn` 클래스 병합) |

> 쉽게: **utils = 어디서나 / lib = 설정만 맞추면 / components = 디자인 같으면 / domain = 절대 못 가져감**(여기에 우리 서비스 지식이 다 들어있음). 의존은 위에서 아래로만, 거꾸로 import 금지.

### 폴더 규칙

- **목적이 곧 폴더**: `무엇을 하는가`로 나눈다 — 설정값=`constants/`, 순수 유틸=`utils/`,
  데이터=`data/`, 도메인 로직=`domain/`, 외부 연동=`lib/`. 포괄 폴더(`core/`, `misc/`) 금지.
- **lib은 외부 연동 전용**: SDK·인프라 어댑터만. 도메인 계산·데이터·유틸을 `lib/`에 섞지 않는다.
- **의존은 한 방향**: `app·components → domain → data·constants → utils·lib`. 역방향 import 금지
  (순수 유틸이 도메인을 참조하지 않는다).
- **components는 도메인 단일 축**: `ui/`(shadcn) · `layout/`(전역 네비) · `shared/`(2개+ 도메인 재사용) +
  도메인 폴더. 한 도메인 전용이면 그 도메인 폴더에, 2개+ 도메인에서 쓰면 `shared/`에 둔다.
  콜로케이션(`app/<route>/_components`) 금지 — 중앙 집중 구조로 import 그래프가 소유관계를 설명하게 한다.
  `domain/`·`scripts/`도 같은 원칙으로 접두사/단계별 폴더로 묶되, 단일 파일은 root에 둔다.
- **대용량 데이터는 번들 밖**: `data/`의 대용량 원본 JSON은 통째로 `import`하지 말고, 빌드타임
  스크립트로 런타임에 쓸 slim 서브셋만 뽑아 그걸 `import`한다. 소비 페이지는 `dynamicParams = false`로
  정적 생성만 한다(배포 가이드의 번들 크기 절 참고). Workers 런타임엔 `fs`가 없으므로 런타임 fs 읽기 금지.

---

## State Management

Zustand & React Query (TanStack Query)

사용 원칙

- Client State는 **Zustand** 사용 (`create` 기반)
- Server/Async Data State는 **React Query** 사용
- Global State는 최소화하고 Controller Hook 내부 상태로 격리
- Store는 Feature 내부에 위치시키는 것을 권장

---

## Routing

Next.js App Router (`next/navigation`)

규칙

- Typed Route 사용 권장
- Navigation Logic은 Custom Hook으로 분리

---

## Local Storage

LocalStorage & IndexedDB (idb / localforage)

사용 목적

- 최근 작업 및 프로젝트 저장
- 최근 문구 및 앱 설정
- 오프라인 캐시

RDBMS/Complex DB는 MVP에서 지양하며 브라우저 스토리지를 활용한다.

---

## UI & Styling

Tailwind CSS & Shadcn UI (Radix UI)

스타일링

Tailwind CSS

아이콘

Lucide React / React Icons (SVG 기반)

애니메이션

Framer Motion / Lottie-react

컴포넌트 패턴

Bottom Sheet / Drawer 패턴 적극 활용 (iOS 인앱 감성)

---

## SEO (중요)

이 프로젝트는 **웹 검색 유입이 핵심 채널**이다. 단일 언어(한국어) 정적 export(SSG) 위에서 아래 규칙을 **반드시** 지킨다.

### 원칙

- **모든 색인 대상 페이지는 서버 컴포넌트로 렌더**한다. 콘텐츠(제목·본문·이미지)가 초기 HTML에 존재해야 크롤러가 읽는다. 인터랙션만 client component로 분리한다.
- **개인/유틸 페이지는 `robots: { index: false }`** 로 색인에서 뺀다 (예: `saved`, `settings`).

### Metadata

- **루트 레이아웃(`app/layout.tsx`)** 에 공통 metadata를 둔다: `metadataBase`(절대 URL 기준), `title.template`(`"%s · Brand"`), 기본 `description`, `openGraph`, `twitter`, `robots`.
  - `title.template` 을 쓰므로 **하위 페이지 title 에는 브랜드 접미사를 붙이지 않는다** (중복 방지).
- **각 라우트는 `generateMetadata`** 로 title·description·canonical·openGraph를 생성한다. 동적 라우트(`place/[id]`, `[category]`)도 동일.
- 배포 도메인은 `constants/site.ts`의 `SITE_URL`(env `NEXT_PUBLIC_SITE_URL`) 한 곳에서만 관리한다. 하드코딩 금지.

### 필수 라우트 파일

- `app/sitemap.ts` — 전 라우트 URL (`dynamic = "force-static"`).
- `app/robots.ts` — 크롤 정책 + sitemap 위치 (`dynamic = "force-static"`).

### 구조화 데이터 (JSON-LD)

- 상세 페이지(`place/[id]`)는 `schema.org` 타입(`Restaurant`/`TouristAttraction`/`Event`)을 `<script type="application/ld+json">` 으로 넣는다.
- 목록/홈은 여력 시 `ItemList` / `BreadcrumbList` 추가 검토.

---

## 에러 / 404 페이지

정적 export + 정적 호스트 기준. 서버 렌더가 없으므로 아래 파일 구성을 지킨다.

- **`app/not-found.tsx`** (서버 컴포넌트) — 정적 호스트가 **미매칭 경로에 서빙하는 `out/404.html`** 이 여기서 나온다. 반드시 존재해야 함. 라우트 내부의 `notFound()`(예: 없는 `place/[id]`)도 이 화면을 받는다.
- **`app/error.tsx`** (`'use client'` 필수) — 라우트 런타임 에러 바운더리. `reset()` 재시도 버튼 제공. `console.error` 자리에 추후 Sentry 연동.
- **`app/global-error.tsx`** (`'use client'` 필수) — 루트 레이아웃까지 실패한 최후 폴백. 자체 `<html>/<body>` 를 렌더한다.
- **공통 레이아웃**은 `components/shared/StatusScreen.tsx`(순수 프레젠테이션, 서버/클라 양쪽 재사용)로 통일한다. 아이콘 + 상태 코드 + 제목/설명 + 액션 버튼(`components/ui/button`).
- 404/에러는 **색인 대상 아님** — sitemap 에 넣지 않는다.

### 체크리스트 (새 라우트 추가 시)

1. 서버 컴포넌트로 콘텐츠 렌더했는가?
2. `generateMetadata` 로 title·description·canonical 넣었는가? (브랜드 접미사 없음)
3. `app/sitemap.ts` 에 경로 추가했는가?
4. 개인/유틸 페이지면 `robots: { index: false }` 넣었는가?

---

## 접근성 (a11y)

- **포커스 가시성**: 전역 `:focus-visible` 링을 `globals.css` 에 정의(키보드 탐색 필수, WCAG 2.4.7). 개별 요소에서 `outline-none` 으로 죽이지 말 것. 커스텀이 필요하면 `focus-visible:` 유틸로 대체 표시.
- **hover 피드백**: `@media (hover: hover)` 로 마우스 환경에서만 버튼/링크 hover 전환을 전역 적용(터치 sticky-hover 방지). 개별 컴포넌트마다 반복하지 않는다.
- **모션 최소화**: `@media (prefers-reduced-motion: reduce)` 전역 처리(WCAG 2.3.3).
- **아이콘 전용 버튼**엔 `aria-label` 필수. 이미지엔 의미 있는 `alt`.
- **폼 요소**엔 `aria-label` 또는 `<label>` 연결(placeholder 만으로 대체 금지).
- **네비게이션 현재 위치**는 `aria-current="page"` 로 표시(색상만으로 구분 금지).
- 클릭 핸들러는 `<button>`/`<a>` 에만 — `div`/`span onClick` 금지(키보드 접근 불가).
- 색 대비는 WCAG AA(본문 4.5:1) 이상. 저대비 토큰(`--disabled`)을 본문 텍스트에 쓰지 않는다.

---

## Theme

Tailwind CSS + `next-themes`를 기반으로 하되,

웹 느낌을 줄이고 **iOS Cupertino / Native App 감성**을 적극 활용한다.

---

## Assets

이미지는 WebP / SVG 우선

PNG 사용 최소화

Lottie 애니메이션 적극 활용

Next.js `<Image/>` 컴포넌트로 최적화(정적 export 시 `unoptimized` 필요).

---

## 성능

목표

첫 콘텐츠 렌더 (FCP)

2초 이하

이미지 처리/저장

3초 이하

화면 전환/스크롤

60fps 유지

불필요한 Re-render 금지 (`useCallback`, `useMemo` 적절 활용)

---

## 네트워크

정적 export(SSG) + 클라이언트 캐싱을 기본으로 한다.

서버 데이터는 Route Handler(`app/api/`)로 프록시·캐싱한 뒤 사용한다.

---

## 코드 스타일

항상

- SOLID
- DRY
- KISS
- Clean Code

를 따른다.

---

## 네이밍 규칙

파일

camelCase 또는 kebab-case (컴포넌트는 PascalCase)

클래스/인터페이스/타입

PascalCase

변수 / 함수 / Hooks

camelCase (`use` Prefix 필수)

상수

UPPER_SNAKE_CASE

Enum

PascalCase

---

## Component 작성 규칙

Functional Component 우선

Custom Hook을 활용한 Logic 분리

Component는 200줄 이하 권장

하나의 Component는 하나의 역할만 수행한다.

기본은 **Server Component**, 사용자 입력·브라우저 API가 필요할 때만 `'use client'`.

---

## 에러 처리

모든 비동기 작업은

try-catch

사용자 친화적 Toast / Alert Message

Sentry Logging (선택)

을 반드시 구현한다.

---

## 테스트

Vitest + React Testing Library (Unit / Component Test) · Playwright (E2E)

- 도메인 로직은 순수 함수로 두어 입출력 단위 테스트를 우선한다.
- 외부 API·기기 입력에 의존하는 기능은 **테스트용 더미/목(mock) 데이터를 코드로 생성**해 에셋 번들 없이 검증한다.
- 데이터 파이프라인(`scripts/`)은 검증 스크립트(`scripts/test/`)로 회귀를 막는다.

---

## AI 개발 규칙

AI는 항상 아래 원칙을 따른다.

- Next.js Stable 버전만 사용한다.
- 새로운 라이브러리를 추가하기 전에 기존 패키지/Next.js 내장 기능으로 해결 가능한지 먼저 검토한다.
- 목적별 레이어(Purpose-first) 구조를 유지한다 (`app·components → domain → data·constants → utils·lib`).
- 코드 중복을 최소화한다.
- 재사용 가능한 UI Component를 우선 작성한다.
- SEO(서버 컴포넌트 렌더·metadata·canonical)를 항상 고려한다.
- SVG 아이콘을 우선 사용한다.
- 성능을 항상 고려한다 (불필요한 리렌더링 방지).
- 한 파일이 300줄을 넘으면 분리를 검토한다.
- 최신 Next.js 공식 권장 방식을 우선 적용한다.

---

## 기술 철학

이 프로젝트는 화려한 기술보다 **사용자 경험(UX)** 과 **SEO** 를 우선한다.

새로운 기능을 추가할 때는 아래 기준을 따른다.

1. Next.js / Web 기본 기능으로 구현 가능한가?
2. 무료 라이브러리로 해결 가능한가?
3. SEO(초기 HTML 콘텐츠)를 해치지 않는가?
4. 유지보수가 쉬운가?
5. AI가 이해하기 쉬운 구조인가?

위 조건을 만족하는 경우에만 새로운 기술을 도입한다.
