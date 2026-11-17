---
title: 공통 기능 구현 메모
type: reference
description: Next.js 앱에 설정 화면, 공유, 리뷰 유도, 정책 링크 등 반복 구현 패턴을 붙일 때 읽는다. 공통 UI/UX·예외 처리 규칙이 필요할 때도 읽는다.
related:
  - ./TECH.md
  - ./DESIGN.md
---

# 공통 기능 구현 메모 (Next.js)

이 문서는 **Next.js (App Router)** 웹 프로젝트에서 반복해서 구현하는 공통 패턴을 정리한다. 단일 언어(한국어) 앱 기준이며 Web API를 활용한다.

---

## 1. 기준 원칙

- **브라우저 기능 추상화**: 공유·외부 링크·메일 등은 Web API(`navigator.share`, `window.open`, `mailto:`)로 구현하고, 미지원 브라우저를 위한 fallback을 둔다.
- **UI/UX 가이드라인**: iOS 인앱 감성을 위해 Tailwind CSS, Lucide React / Radix UI(Shadcn UI)를 활용하며, **Drawer / Bottom Sheet** 패턴을 우선 적용한다.
- **Non-blocking 안전장치**: 설정 저장, 공유, 리뷰 유도 등 보조 기능의 오류가 메인 작업 흐름을 막지 않도록 `try-catch`와 토스트(Toast) 메시지로 예외 처리한다.

---

## 2. 설정 화면 (Settings View)

> **옵션**: 설정 화면은 프로젝트마다 필요 없을 수 있음 (테마 스위처 등이 없는 앱이면 생략).

라벨은 한국어로 고정 표기하고, 설정 항목을 구성한다.

```tsx
// components/settings/SettingsView.tsx
"use client";
import React from "react";
import {
  Moon,
  Share2,
  Star,
  ShieldCheck,
  FileText,
  Mail,
} from "lucide-react";
import { useSettingsStore } from "@/store/useSettingsStore";
import { shareApp } from "@/lib/web/share";
import { openExternalUrl, openContactEmail } from "@/lib/web/browser";

interface SettingsViewProps {
  onRateApp: () => void;
  onOpenThemeSheet: () => void;
}

export const SettingsView = ({
  onRateApp,
  onOpenThemeSheet,
}: SettingsViewProps) => {
  const { theme } = useSettingsStore();

  return (
    <div className="max-w-md mx-auto p-4 space-y-6 pb-12">
      {/* 화면 섹션 */}
      <section>
        <h2 className="text-xs font-semibold text-gray-500 uppercase px-3 mb-2">
          화면
        </h2>
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 divide-y divide-gray-100 dark:divide-gray-700">
          <SettingsTile
            icon={<Moon className="w-5 h-5 text-indigo-500" />}
            title="화면 모드"
            value={
              theme === "system" ? "시스템" : theme === "dark" ? "다크" : "밝게"
            }
            onClick={onOpenThemeSheet}
          />
        </div>
      </section>

      {/* 지원 섹션 */}
      <section>
        <h2 className="text-xs font-semibold text-gray-500 uppercase px-3 mb-2">
          지원
        </h2>
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 divide-y divide-gray-100 dark:divide-gray-700">
          <SettingsTile
            icon={<Share2 className="w-5 h-5 text-green-500" />}
            title="앱 공유하기"
            onClick={() => shareApp("이 앱을 추천합니다!")}
          />
          <SettingsTile
            icon={<Star className="w-5 h-5 text-amber-500" />}
            title="평가 및 리뷰"
            onClick={onRateApp}
          />
        </div>
      </section>

      {/* 정보 섹션 */}
      <section>
        <h2 className="text-xs font-semibold text-gray-500 uppercase px-3 mb-2">
          정보
        </h2>
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 divide-y divide-gray-100 dark:divide-gray-700">
          <SettingsTile
            icon={<ShieldCheck className="w-5 h-5 text-gray-500" />}
            title="개인정보처리방침"
            onClick={() => openExternalUrl("https://example.com/privacy")}
          />
          <SettingsTile
            icon={<FileText className="w-5 h-5 text-gray-500" />}
            title="이용약관"
            onClick={() => openExternalUrl("https://example.com/terms")}
          />
          <SettingsTile
            icon={<Mail className="w-5 h-5 text-gray-500" />}
            title="문의하기"
            value="support@example.com"
            onClick={openContactEmail}
          />
        </div>
      </section>
    </div>
  );
};

const SettingsTile = ({
  icon,
  title,
  value,
  onClick,
}: {
  icon: React.ReactNode;
  title: string;
  value?: string;
  onClick: () => void;
}) => {
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors text-left"
    >
      <div className="flex items-center gap-3 min-w-0">
        <div className="p-1.5 rounded-lg bg-gray-100 dark:bg-gray-700 flex-shrink-0">
          {icon}
        </div>
        <span className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
          {title}
        </span>
      </div>
      <div className="flex items-center gap-2 flex-shrink-0 ml-2">
        {value && (
          <span className="text-sm text-gray-400 dark:text-gray-500">
            {value}
          </span>
        )}
        <span className="text-gray-300 dark:text-gray-600 text-lg">›</span>
      </div>
    </button>
  );
};
```

---

## 3. 테마 및 설정 상태 Persistence (Zustand + localStorage)

> **옵션**: 상태 persist 는 프로젝트마다 필요 없을 수 있음 (저장할 사용자 설정이 없으면 생략).

테마 등 앱 상태 저장을 위해 Zustand `persist`를 localStorage와 연동한다.

```ts// store/useSettingsStore.ts
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

interface SettingsState {
  theme: "system" | "light" | "dark";
  setTheme: (theme: "system" | "light" | "dark") => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      theme: "system",
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: "app-settings",
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
```

---

## 4. 공유 · 외부 링크 (Web API)

Web Share API를 우선 사용하고, 미지원 브라우저에서는 클립보드 복사로 폴백한다.

```ts// lib/web/share.ts
export async function shareApp(message: string) {
  const shareData = {
    title: "앱 추천",
    text: message,
    url: "https://example.com",
  };

  try {
    if (navigator.share) {
      await navigator.share(shareData);
    } else {
      await navigator.clipboard.writeText(
        `${shareData.text}\n${shareData.url}`,
      );
      alert("링크가 클립보드에 복사되었습니다.");
    }
  } catch (e) {
    // 사용자가 공유 취소 시 에러 무시
  }
}

// lib/web/browser.ts
export function openExternalUrl(url: string) {
  try {
    window.open(url, "_blank", "noopener,noreferrer");
  } catch (e) {
    console.error("URL 열기 실패:", e);
  }
}

export function openContactEmail() {
  window.location.href = "mailto:support@example.com";
}
```

---

## 5. 리뷰 유도 정책 (In-App Review)

> **옵션**: 리뷰 유도는 프로젝트마다 필요 없을 수 있음 (스토어 앱·리뷰 페이지가 없으면 생략).

웹에는 네이티브 인앱 리뷰 API가 없으므로 스토어/리뷰 페이지 링크로 유도한다. 자동 유도는 사용자가 핵심 과업(예: 3회 이상 작업 성공)을 마친 후에만 노출한다.

```ts// lib/web/reviewPolicy.ts
export interface ReviewPromptState {
  successCount: number;
  hasClickedReview: boolean;
  lastShownAt: string | null;
}

export function shouldShowReviewPrompt(state: ReviewPromptState): boolean {
  if (state.hasClickedReview) return false;
  if (state.successCount < 3) return false;
  if (!state.lastShownAt) return true;

  const lastShown = new Date(state.lastShownAt);
  const now = new Date();

  // 하루에 한 번만 표시
  return lastShown.toDateString() !== now.toDateString();
}
```

---

## 6. 설정 내 정보/정책 페이지 & shadcn 버튼 (모든 앱 공통)

설정(Settings) 화면에는 **앱 공유 아래에 정보/정책 네비게이션**을 두고, 각 항목을 누르면 하위 페이지(`settings/privacy`, `settings/terms`, `settings/contact` 등)로 이동한다. **개인정보처리방침 링크는 EU/GDPR 대응상 사실상 필수**이므로 모든 앱에서 동일하게 구현한다.

정보/정책 텍스트와 UI 라벨은 한국어로 고정 표기한다(법적 문서 성격).

> **옵션**: 개인정보처리방침은 필수, 이용약관·문의(terms/contact)는 프로젝트마다 필요 없을 수 있음. 설정 화면(§2)이 없으면 정책 링크는 푸터 등에 둬도 된다.

### 6-1. 라우트 구조 (App Router)

```text
app/settings/
├── page.tsx            # 설정 메인 (테마/공유 + 정보 네비)
├── privacy/page.tsx    # 개인정보처리방침
├── terms/page.tsx      # 이용약관
└── contact/page.tsx    # 문의하기 (mailto)
```

- 공용 셸(`InfoPage`)로 뒤로가기 헤더 + 본문을 통일한다.

```tsx
// components/shared/InfoPage.tsx (Server Component)
export const InfoPage = ({
  title,
  backHref,
  children,
}: {
  title: string;
  backHref: string;
  children: React.ReactNode;
}) => (
  <div className="mx-auto flex w-full max-w-2xl flex-col gap-4 p-4">
    <div className="flex items-center gap-1">
      <Button variant="ghost" size="icon" asChild>
        <Link href={backHref} aria-label="back">
          <ChevronLeft className="h-5 w-5" />
        </Link>
      </Button>
      <h1 className="text-xl font-bold">{title}</h1>
    </div>
    <div className="flex flex-col gap-3 text-sm leading-6 text-secondary">
      {children}
    </div>
  </div>
);
```

### 6-2. shadcn 버튼 (비파괴적 도입)

> ⚠️ **`npx shadcn init` 은 `globals.css` 의 커스텀 디자인 토큰을 덮어쓴다.** 이미 `docs/DESIGN.md` 기반 토큰(`--surface`, `--secondary`, `--accent-*` 등)을 쓰는 프로젝트에서는 init 대신 **shadcn 패턴(cva + cn + Radix `Slot`)만 이식**한다.

```bash
npm i class-variance-authority clsx tailwind-merge @radix-ui/react-slot
```

```ts// core/utils/cn.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export const cn = (...inputs: ClassValue[]): string => twMerge(clsx(inputs));
```

```tsx
// components/ui/button.tsx — 변형은 프로젝트 토큰에 맞춤. asChild 로 <Link> 도 버튼화.
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 ...",
  {
    variants: {
      variant: {
        default: "bg-foreground text-background hover:opacity-90",
        accent: "bg-accent-blue text-white hover:opacity-90",
        ghost: "hover:bg-black/5 dark:hover:bg-white/5",
        outline: "border border-black/10 dark:border-white/15 ...",
      },
      size: {
        default: "h-11 rounded-full px-5",
        icon: "size-10 rounded-full",
        row: "h-auto w-full justify-between rounded-none px-4 py-3.5 font-medium", // 리스트 행
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);

export const Button = ({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: ButtonProps) => {
  const Comp = asChild ? Slot : "button";
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
};
```

### 6-3. 설정 네비게이션 (액션 + 링크 혼합)

한 카드(`divide-y`) 안에 **공유(onClick 액션)** 와 **정보 페이지 링크(asChild + `<Link>`)** 를 함께 배치한다.

```tsx
<div className="divide-y divide-black/5 overflow-hidden rounded-2xl bg-surface shadow-sm dark:divide-white/10">
  {/* 액션: onClick */}
  <Button variant="ghost" size="row" onClick={() => shareApp(msg)}>
    <span className="flex items-center gap-3">
      <Share2 className="h-5 w-5" />앱 공유
    </span>
  </Button>

  {/* 링크: asChild + Link → settings/{slug} 이동 */}
  {infoLinks.map(({ slug, icon: Icon, label }) => (
    <Button key={slug} variant="ghost" size="row" asChild>
      <Link href={`/settings/${slug}`}>
        <span className="flex items-center gap-3">
          <Icon className="h-5 w-5 text-secondary" />
          {label}
        </span>
        <ChevronRight className="h-4 w-4 text-disabled" />
      </Link>
    </Button>
  ))}
</div>;

// 라벨 한국어 고정
const infoLinks = [
  { slug: "privacy", icon: ShieldCheck, label: "개인정보처리방침" },
  { slug: "terms", icon: FileText, label: "이용약관" },
  { slug: "contact", icon: Mail, label: "문의하기" },
] as const;
```

### 6-4. 체크리스트

- [ ] 설정에 개인정보처리방침 링크가 존재하는가? (GDPR/정책 대응)
- [ ] 정보 페이지에서 뒤로가기가 동작하는가?
- [ ] shadcn 은 init 없이 패턴만 이식해 기존 디자인 토큰을 보존했는가?
- [ ] 문의하기는 `mailto:` 링크로 기본 메일 앱을 여는가?

---

## 7. 저장소 동의 배너 (EU/GDPR 대응)

로컬 저장소(localStorage)·향후 광고/분석을 쓰는 앱은 **최초 진입 시 동의 배너**를 노출한다. 특히 EU 대상 서비스는 ePrivacy/GDPR 상 필요하다.

> **원칙**: 필수(기능) 저장은 동의와 무관하게 동작한다. 배너는 **고지 + 선택적(분석/광고) 항목 동의 기록**용이며, `accepted` 플래그로 향후 Analytics 초기화를 게이팅한다.

### 7-1. 동의 상태 store (Zustand + localStorage)

```ts// data/local/consentStore.ts
export const useConsentStore = create<ConsentState>()(
  persist(
    (set) => ({
      decided: false, // 배너에서 선택했는지
      accepted: false, // 선택적 항목 동의 여부 (분석/광고 게이팅용)
      setConsent: (accepted: boolean) => set({ decided: true, accepted }),
    }),
    { name: "<app>-consent", storage: createJSONStorage(() => localStorage) },
  ),
);
```

> **옵션**: zustand store 는 프로젝트마다 필요 없을 수 있음 (동의 플래그만 쓰면 store 없이 구현 가능).

### 7-2. 배너 컴포넌트

- `persist` 는 클라이언트에서만 rehydrate → **마운트 전엔 렌더하지 않아** 깜빡임/hydration 불일치를 막는다.
- 위치는 하단(`fixed bottom-4` 또는 네비 위), z-index 는 네비보다 위.
- 개인정보처리방침 링크(§6) 포함, 문구는 한국어로 고정 표기.

```tsx
// components/consent/ConsentBanner.tsx
"use client";
export const ConsentBanner = () => {
  const decided = useConsentStore((s) => s.decided);
  const setConsent = useConsentStore((s) => s.setConsent);

  const [hydrated, setHydrated] = useState(false);
  useEffect(() => setHydrated(true), []);
  if (!hydrated || decided) return null;

  return (
    <div className="fixed inset-x-3 bottom-4 z-50 mx-auto max-w-2xl rounded-2xl bg-surface p-4 shadow-xl ...">
      <p className="text-xs text-secondary">
        최근 조회·설정을 브라우저에 저장합니다. 광고나 추적은 없습니다.{" "}
        <Link href="/settings/privacy">개인정보처리방침</Link>
      </p>
      <div className="mt-3 flex justify-end gap-2">
        <Button variant="outline" size="sm" onClick={() => setConsent(false)}>
          필수만
        </Button>
        <Button variant="accent" size="sm" onClick={() => setConsent(true)}>
          확인
        </Button>
      </div>
    </div>
  );
};
```

`app/layout.tsx` 에 마운트한다.

### 7-3. 체크리스트

- [ ] 최초 진입 시 배너가 뜨고, 선택 후 재노출되지 않는가? (localStorage 저장)
- [ ] 필수 기능(최근 조회/테마)은 거부해도 정상 동작하는가?
- [ ] 배너 문구가 실제 저장 내용과 일치하는가? (개인정보처리방침과 정합)
- [ ] Analytics(GA4, §8)는 Consent Mode 기본 `denied` 로 로드되고, `accepted === true` 일 때만 `granted` 로 갱신되는가? (동의 전 쿠키 미저장)

---

## 8. Google Analytics (GA4) — Consent Mode v2

> **옵션**: GA4 는 프로젝트마다 필요 없을 수 있음 (`NEXT_PUBLIC_GA_ID` 미설정이면 미로드 = 무동작).

GA4(gtag.js)를 로드하되 **Consent Mode v2** 로 동의 신호를 게이팅한다. `NEXT_PUBLIC_GA_ID` 가 있으면 gtag 를 **항상 로드**하고, 동의 전엔 기본 `denied`(쿠키 없이 익명 모델링 신호만 수집), 배너 수락 시 `granted` 로 갱신한다. 동의 전 쿠키 미저장이라 ePrivacy/GDPR 사전동의를 충족하면서 `denied` 구간의 익명 트래픽까지 모델링으로 회수한다.

> ⚠️ 과거엔 `accepted` 가 참일 때만 gtag 를 **로드**했다(동의 전 데이터 0, `@next/third-parties` 조건부 마운트). Consent Mode 는 gtag 를 먼저 올리고 **동의 신호만** denied→granted 로 바꾼다. 동의 default(denied)는 반드시 `config` 보다 **먼저** 실행돼야 하므로 같은 인라인 스크립트에서 순서로 보장한다.

### 8-1. gtag 로더 + Consent 갱신 (`Analytics.tsx`)

```tsx
// components/shared/Analytics.tsx
"use client";
import { useEffect } from "react";
import Script from "next/script";
import { useConsentStore } from "@/data/local/consentStore";

export const Analytics = () => {
  const accepted = useConsentStore((s) => s.accepted);
  const gaId = process.env.NEXT_PUBLIC_GA_ID; // G-XXXXXXXXXX, 브라우저 노출 → NEXT_PUBLIC_ 필수
  const enabled = Boolean(gaId);

  // 수락 시 granted 로 갱신. dataLayer 에 직접 push → gtag.js 로드 순서·persist rehydrate 방어.
  useEffect(() => {
    if (!enabled || !accepted) return;
    const w = window as Window & { dataLayer?: unknown[] };
    w.dataLayer = w.dataLayer || [];
    function gtag(..._args: unknown[]) {
      w.dataLayer!.push(arguments);
    }
    gtag("consent", "update", {
      ad_storage: "granted",
      ad_user_data: "granted",
      ad_personalization: "granted",
      analytics_storage: "granted",
    });
  }, [enabled, accepted]);

  if (!enabled) return null;
  return (
    <>
      {/* consent default(denied) 는 config 보다 먼저 — 같은 스크립트 내 순서로 보장 */}
      <Script id="ga-init" strategy="afterInteractive">{`
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});
        gtag('set', 'url_passthrough', true);    // gclid/utm 을 쿠키 대신 URL 로 전달(denied 유입경로 보존)
        gtag('set', 'ads_data_redaction', true); // denied 시 광고 식별자 마스킹(준수 안전장치)
        gtag('js', new Date());
        gtag('config', '${gaId}');
      `}</Script>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}
        strategy="afterInteractive"
      />
    </>
  );
};
```

- `app/layout.tsx` 에서 `<ConsentBanner/>`(§7) 옆에 마운트. 배너 **수락(accept)** → `accepted=true` → useEffect 가 `consent update granted` push. `consentStore` 는 persist 라 재방문에도 유지(재방문 수락 유저도 effect 가 granted 재전송).
- **env 키**: `NEXT_PUBLIC_GA_ID`(`.env`, gitignore). `NEXT_PUBLIC_*` 는 **빌드타임에 값이 박히므로** CI/배포 호스트 env 에도 등록해야 프로덕션에서 잡힌다(로컬 `.env` 만으론 프로덕션 미반영). `@next/third-parties` 대신 내장 `next/script` 사용(의존성 회피).
- **광고 안 쓰면**: `ad_storage`·`ad_user_data`·`ad_personalization` 은 빼고 `analytics_storage` 만 남겨도 된다.
- **SPA 페이지뷰**: GA4 향상된 측정(Enhanced measurement)의 "브라우저 히스토리 기반 페이지 변경"이 소프트 네비 라우트를 자동 집계 → 수동 `page_view` 전송 생략. 누락되면 그때 `usePathname` 훅으로 명시 전송 추가.
- **denied 구간 수집 범위**: 유입 경로(referrer·utm·채널/소스/매체)는 URL 기반이라 denied 여도 쿠키 없이 수집됨(익명 페이지뷰/이벤트 포함) → "어디서 들어왔는지"는 동의 전에도 잡힘. 단 `_ga` 미저장이라 교차세션 사용자 스티칭 X. 정확 사용자수·전환은 Google 모델링 보정이며, 모델링은 트래픽 임계치(대략 denied 이벤트 7일 일 1000+) 이상에서만 켜짐 → 소규모는 pre-consent 데이터가 집계/제한적. `url_passthrough` 로 광고 클릭(gclid) 유입도 쿠키 없이 URL 로 보존.
- **검증**: DevTools Network 에서 `gtag/js` 로드 확인 → 배너 수락 → `/g/collect` 요청 `gcs` 파라미터가 `G111`(granted) 이면 반영됨. denied 구간은 `G100`.

### 8-2. 체크리스트

- [ ] `NEXT_PUBLIC_GA_ID` 미설정 시 gtag 가 로드되지 않는가? (무동작)
- [ ] 동의 전 Consent Mode 기본 `denied` 로 gtag 가 로드되고 쿠키는 미저장인가? (`/g/collect` `gcs=G100`)
- [ ] 배너 수락 시 `granted` 로 update 되는가? (`gcs=G111`)
- [ ] 재방문 수락 유저도 rehydrate 후 effect 가 granted 재전송하는가?
- [ ] denied 구간(`gcs=G100`)에서 유입 경로(referrer/utm)가 `/g/collect` 요청(`dr`·utm 파라미터)에 실려 가는가?
- [ ] 측정 ID 가 코드가 아닌 `NEXT_PUBLIC_GA_ID` 환경변수로 주입되는가?
- [ ] `_ga`/모델링 쿠키 사용이 개인정보처리방침·배너 문구에 반영됐는가?

---

## 9. AI 코딩 에이전트 설정 (Next.js, 모든 앱 공통)

> 출처: [Next.js — How to set up your Next.js project for AI coding agents](https://nextjs.org/docs/app/guides/ai-agents)

Next.js 는 **설치된 버전과 일치하는 문서를 `next` 패키지 안에 번들**한다(`node_modules/next/dist/docs/`). AI 코딩 에이전트가 학습 데이터(구버전) 대신 이 번들 문서를 참조하도록 프로젝트를 설정한다. 핵심은 4단계: ① 번들 문서로 안내 ② 런타임 가시성 제공 ③ 에러가 수정을 주도 ④ 다단계 작업은 Skill 로.

### 9-1. Step 1 — 번들 문서로 에이전트 안내 (`AGENTS.md`)

프로젝트 루트 `AGENTS.md` 가 번들 문서(`node_modules/next/dist/docs/`, 구조는 nextjs.org/docs 와 동일)를 가리키게 한다. 대부분 에이전트(Claude Code, Codex, Cursor, GitHub Copilot)가 세션 시작 시 `AGENTS.md` 를 자동으로 읽는다. 문서는 네트워크 없이 항상 설치 버전과 일치하며, `next` 업그레이드 시 문서도 함께 업그레이드된다.

- **신규 프로젝트**: `create-next-app` 이 `AGENTS.md` + `CLAUDE.md` 자동 생성(원치 않으면 `--no-agents-md`).
- **기존 프로젝트 (16.3+)**: `next dev` 실행 시 에이전트 환경이 감지되고 managed block 이 없으면 `AGENTS.md` + `CLAUDE.md` 자동 생성. 기존 파일은 **upsert** — managed block 밖의 내용은 보존된다.

```md
<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes ... Read the relevant guide in
`node_modules/next/dist/docs/` before writing any code.

<!-- END:nextjs-agent-rules -->
```

```md
// CLAUDE.md
@AGENTS.md
```

- 프로젝트별 지침은 **`<!-- BEGIN/END:nextjs-agent-rules -->` 마커 밖에** 작성 → Next.js 가 managed block 갱신해도 보존된다.
- managed block 은 `next dev` 가 다시 써넣으므로 diff 에서 지워도 재생성 → **커밋해서 트리를 깨끗하게** 유지.
- **opt-out**: `next.config.ts` 에 `agentRules: false`. (단, [nextjs.org/evals](https://nextjs.org/evals) 벤치마크상 켜두는 게 유리 → 기본 유지 권장.)
- **16.2**: 문서는 번들되나 `AGENTS.md` 자동 생성 X → 수동 작성. **16.1 이하**: `npx @next/codemod@canary agents-md` 로 `.next-docs/` 에 버전 일치 사본 다운로드.
- **네트워크 경유**: nextjs.org/docs 의 모든 페이지 URL 뒤에 `.md` 를 붙이면 마크다운. 인덱스는 [`/docs/llms.txt`](https://nextjs.org/docs/llms.txt), 단일 파일은 `/docs/llms-full.txt` (llms.txt 규약).

### 9-2. Step 2 — 런타임 가시성

`next dev` 를 띄우고 에이전트가 실행 중 서버 대상으로 작업하게 한다(에이전트는 브라우저를 못 봄).

- `next dev` 가 **브라우저 콘솔 에러/경고를 터미널로 포워딩**(`logging.browserToTerminal`) → 에이전트가 읽는 출력에 클라이언트 실패가 포함됨.
- `next dev` 는 PID·포트·URL 을 `.next/dev/lock` 에 기록 → 두 번째 `next dev` 는 중복 실행 대신 기존 서버 URL 을 알려줌.
- **프레임워크 뷰**: [Next.js MCP 서버](https://nextjs.org/docs/app/guides/mcp) `/_next/mcp` — 라우트·서버 로그·컴파일 이슈 노출. `get_compilation_issues` / `compile_route` 로 `next build` 없이 컴파일 확인.
- **브라우저 뷰**: [`agent-browser`](https://github.com/vercel-labs/agent-browser) — DOM·콘솔·네트워크·Web Vitals 를 구조화 텍스트로. React DevTools 켜면 컴포넌트 트리·Suspense 상태까지.

### 9-3. Step 3 — 에러가 수정을 주도

[Cache Components](https://nextjs.org/docs/app/getting-started/caching) 활성 시 blocking 에러가 **라벨된 수정안**(각기 다른 trade-off)을 제시. 오버레이의 **Copy prompt** 버튼이 붙여넣기용 프롬프트로 패키징(해당 에러 페이지 읽기 → 정석 패턴 적용 → 런타임 검증 순서). 동일 메뉴가 `next dev` 터미널·`next build` 출력에도 찍혀 CI 로그를 읽는 에이전트도 봄. `Learn more` 링크는 에이전트용으로 작성된 [`/docs/messages`](https://nextjs.org/docs/messages) 페이지로 연결.

### 9-4. Step 4 — 다단계 작업은 Skill 로

프레임워크 지식은 Skill 이 아니라 번들 문서에서 온다(항시 컨텍스트 > 온디맨드 검색). Skill 은 조회가 아닌 **워크플로**용(Cache Components / Partial Prefetching 도입 등). [github.com/vercel/next.js/tree/canary/skills](https://github.com/vercel/next.js/tree/canary/skills), [skills.sh/vercel/next.js](https://www.skills.sh/vercel/next.js).

- **`next-dev-loop`** — 실행 서버 대상 inspect→edit→verify 루프. `npx skills add vercel/next.js --skill next-dev-loop`
- **`next-cache-components-adoption`** — Cache Components 마이그레이션(기능별 점진 + 체크인).
- **`next-cache-components-optimizer`** — 대상 라우트를 `instant()` 실패 테스트 기준으로 리팩터.
- **`next-partial-prefetching-adoption`** — Partial Prefetching(App Shell 공유)로 이전.

### 9-5. 체크리스트

- [ ] 루트에 `AGENTS.md` 존재 + managed block 이 번들 문서를 가리키는가?
- [ ] `CLAUDE.md` 가 `@AGENTS.md` 로 참조하는가?
- [ ] 프로젝트별 지침은 managed 마커 **밖**에 있어 갱신 시 보존되는가?
- [ ] managed block 을 diff 에서 지우지 않고 **커밋**하는가?
- [ ] (16.3+) 자동 생성에 맡기거나, 구버전이면 수동/codemod 로 문서 안내를 넣었는가?

---

## 10. 헤더 네비게이션 (Desktop / Mobile 분기)

헤더는 **단일 데이터 배열(`headerLink`)** 을 `app/layout.tsx` 에서 정의하고, 데스크탑·모바일 두 컴포넌트가 **같은 배열을 공유**해 렌더한다. 메뉴를 추가/변경할 때 배열 한 곳만 고치면 양쪽에 반영된다. 반응형 분기는 JS 가 아니라 **Tailwind `hidden` / `lg:` 유틸리티**로 처리해, 둘 다 서버에서 렌더되고 뷰포트에 맞는 쪽만 보인다(hydration 안전·SEO 링크 둘 다 HTML 에 존재).

### 10-1. 데이터 모델 (shared type)

메뉴 항목은 공유 타입으로 정의한다. 2뎁스(드롭다운/서브메뉴)만 지원한다.

실제 구현에서는 각 메뉴와 하위 메뉴에 **기능을 나타내는 Lucide 아이콘을 반드시 추가**한다. 공유 메뉴 데이터에 직렬화 가능한 `icon` 키를 두고, 공통 아이콘 컴포넌트에서 매핑해 데스크탑·모바일이 같은 아이콘을 사용한다. 서버에서 클라이언트로 메뉴 데이터를 전달할 때 아이콘 컴포넌트 함수 자체를 props로 넘기지 않는다.

```ts
// src/types/index.ts
export interface IHeaderNavigation {
  name: string;
  link: string;
  children?: IHeaderNavigation[]; // 있으면 드롭다운(desktop)·그룹(mobile)
}
```

```tsx
// app/layout.tsx — 데이터 한 곳에서 정의, Header 로 주입
const headerLink: IHeaderNavigation[] = [
  { name: "홈", link: "/" },
  { name: "스터디", link: "/study" },
  { name: "데이터", link: "/data" },
  { name: "백엔드", link: "/backend" },
  { name: "관리자", link: "/admin" },
];

// <Header headerLink={headerLink} /> 로 주입
```

### 10-2. 컨테이너 (두 네비 동시 렌더, CSS 로 택1)

```tsx
// components/Header/Header.tsx
const Header = ({ headerLink }: { headerLink: IHeaderNavigation[] }) => (
  <section className="py-4">
    <div className="container">
      <DesktopNavbar headerLink={headerLink} /> {/* hidden lg:flex */}
      <MobileNavbar headerLink={headerLink} /> {/* lg:hidden */}
    </div>
  </section>
);
```

### 10-3. 데스크탑 (`hidden lg:flex` + shadcn DropdownMenu)

- `nav` 에 `hidden justify-between lg:flex` → **lg 이상에서만** 가로 네비 노출.
- `children` 있으면 **shadcn `DropdownMenu`**(Radix) 로 호버/클릭 드롭다운, 없으면 단순 `<Link>`.
- 링크 스타일은 `navigationMenuTriggerStyle()` 을 `cn()` 으로 재사용해 트리거/링크 외형을 통일.
- 우측에 검색(`HeaderSearch`) + 프로필(`ProfileButton`) 고정.

```tsx
// components/Header/desktop-navbar.tsx (요지)
<nav className="hidden justify-between lg:flex">
  <div className="flex items-center gap-6">
    <Link href="/"><LogoImage ... /></Link>
    <ul className="flex items-center gap-1">
      {headerLink?.map((item) =>
        item.children?.length ? (
          <DropdownMenu key={item.name}>
            <DropdownMenuTrigger className={cn(navigationMenuTriggerStyle(), "text-sm")}>
              {item.name}
              <ChevronDown className="ml-1 h-3 w-3" />
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-48 p-2">
              {item.children.map((child) => (
                <DropdownMenuItem key={child.link} asChild>
                  <Link href={child.link}>{child.name}</Link>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        ) : (
          <li key={item.name}>
            <Link href={item.link} className={cn(navigationMenuTriggerStyle(), "text-sm")}>
              {item.name}
            </Link>
          </li>
        ),
      )}
    </ul>
  </div>
  <div className="flex items-center gap-2">
    <HeaderSearch />
    <ProfileButton />
  </div>
</nav>
```

### 10-4. 모바일 (`lg:hidden` + shadcn Sheet 드로어)

- 래퍼 `lg:hidden` → **lg 미만에서만** 노출. 상단 로고 + 햄버거(`Menu`) 버튼, 하단 검색바.
- 햄버거 탭 → **shadcn `Sheet`**(우측 드로어) 열림. `open` 상태는 로컬 `useState`.
- 드롭다운 대신 **서브메뉴를 평탄화(flatten)** — `children` 그룹은 라벨(헤더) + 들여쓴 링크 목록으로 펼쳐 보인다(모바일은 호버 없음 → 접기 UI 대신 전개).
- 링크 탭 시 `onClick={() => setOpen(false)}` 로 드로어 닫기(§1 "Drawer/Bottom Sheet 우선" 원칙).
- 드로어 하단 고정 영역에 `ProfileButton`(닫기 핸들러 전달).

```tsx
// components/Header/mobile-navbar.tsx (요지)
<div className="flex flex-col gap-3 lg:hidden">
  <div className="flex items-center justify-between">
    <Link href="/"><LogoImage ... /></Link>
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="outline" size="icon" aria-label="메뉴 열기">
          <Menu className="size-4" />
        </Button>
      </SheetTrigger>
      <SheetContent className="overflow-y-auto">
        <SheetHeader>
          <SheetTitle><Link href="/" onClick={() => setOpen(false)}><LogoImage ... /></Link></SheetTitle>
        </SheetHeader>
        <nav className="flex flex-col gap-4 p-4">
          {headerLink.map((item) =>
            item.children?.length ? (
              <div key={item.name} className="flex flex-col gap-3">
                <span className="text-sm font-semibold text-muted-foreground">{item.name}</span>
                {item.children.map((child) => (
                  <Link key={child.link} href={child.link} className="pl-3 ..."
                    onClick={() => setOpen(false)}>
                    {child.name}
                  </Link>
                ))}
              </div>
            ) : (
              <Link key={item.link} href={item.link} className="..." onClick={() => setOpen(false)}>
                {item.name}
              </Link>
            ),
          )}
        </nav>
        {/* 하단 고정: 프로필 */}
        <ProfileButton setMobileNavbarOpen={setOpen} />
      </SheetContent>
    </Sheet>
  </div>
  <HeaderSearch />
</div>
```

### 10-5. 핵심 원칙 요약

- **단일 소스**: 메뉴 배열 1개(`headerLink`)를 양쪽이 공유 → 중복/드리프트 방지.
- **CSS 반응형 분기**: `hidden lg:flex` / `lg:hidden` 으로 택1, 둘 다 서버 렌더 → SEO 링크·접근성 보존.
- **UX 분기**: 데스크탑은 드롭다운(호버/클릭), 모바일은 서브메뉴 평탄화 + 드로어(Sheet).
- **일관 외형**: 데스크탑 링크/트리거는 `navigationMenuTriggerStyle()` 재사용, 모바일은 `onClick` 으로 드로어 자동 닫기.
- **메뉴 아이콘 필수**: 상위 메뉴·드롭다운 항목·모바일 하위 메뉴는 아이콘 + 텍스트로 표시한다. 아이콘은 `size-4 shrink-0`, 텍스트와의 간격은 `gap-2` 또는 `gap-3`으로 통일한다. 장식 아이콘에는 `aria-hidden="true"`를 적용하고, 아이콘만 있는 버튼·링크에는 `aria-label`을 제공한다.
- **공유 primitive**: `DropdownMenu`·`Sheet`·`Button` 은 `@workspace/ui`(shadcn) 에서 가져온다(앱별 중복 구현 금지).

### 10-6. 체크리스트

- [ ] 메뉴 추가 시 `headerLink` 배열 한 곳만 수정해 양쪽에 반영되는가?
- [ ] 모든 메뉴·하위 메뉴에 의미에 맞는 아이콘이 있으며, 데스크탑·모바일에서 동일한 아이콘과 일관된 크기·간격을 사용하는가?
- [ ] 장식 아이콘은 스크린리더에서 제외하고, 아이콘 전용 버튼·링크에는 접근 가능한 이름을 제공했는가?
- [ ] 데스크탑/모바일 네비 모두 초기 HTML(view-source)에 링크가 존재하는가? (SEO)
- [ ] 모바일 드로어에서 링크 탭 시 Sheet 가 닫히는가?
- [ ] 드롭다운/서브메뉴가 2뎁스를 넘지 않는가? (`children` 안에 또 `children` 금지)
- [ ] 햄버거 버튼에 `aria-label` 이 있는가? (a11y)

---

## 11. QA 체크리스트

- [ ] 화면 모드(Dark/Light) 변경이 localStorage 에 저장되는가?
- [ ] Web Share 미지원 브라우저에서 클립보드 폴백이 동작하는가?
- [ ] 서버 컴포넌트로 렌더된 콘텐츠가 초기 HTML(view-source)에 존재하는가? (SEO)
