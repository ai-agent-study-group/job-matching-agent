---
title: 디자인 시스템
type: reference
description: 화면 UI를 만들 때 읽는다. 컬러, 타이포그래피, radius, spacing, 아이콘, 버튼, 카드, Empty State 등 디자인 토큰과 규칙을 찾을 때 읽는다.
related:
    - ./AI_RULES.md
    - ./FEATURE.md
    - ./ANIMATION.md
---

# 디자인 시스템

## 디자인 목표

**LinkedIn 웹 페이지 톤**을 따른다. 채용·커리어 서비스답게 **신뢰감 있고, 정돈되고, 정보가 잘 읽히는** 화면이 목표다.

- 장식보다 **정보 밀도와 가독성**이 우선이다. 사용자는 공고·이력서·매칭 결과를 "읽으러" 온다.
- 웜 그레이 배경 위에 흰 카드를 쌓는 **카드 피드 레이아웃**.
- 색은 **LinkedIn Blue 하나**로 강조한다. 나머지는 무채색.
- 모션은 절제한다. 상태 변화를 알려주는 짧은 전환만 쓴다(`ANIMATION.md`).

## 디자인 키워드

Professional · Trustworthy · Clean · Information-dense · Calm

참고 화면: LinkedIn 피드, 채용공고 목록/상세(Jobs), 프로필 페이지.

---

## 레이아웃

- **배경**: 웜 그레이(`--background`) 전체, 콘텐츠는 흰 카드(`--card`)에 담는다.
- **상단 내비게이션**: 흰 배경 + 하단 1px 보더, sticky. 아이콘 + 짧은 라벨 세로 배치(LinkedIn 글로벌 nav 패턴).
- **컨테이너**: 최대 너비 `max-w-6xl` 중앙 정렬. 데스크톱은 그리드 열 구성.
  - 목록/상세: 왼쪽 목록(좁게) + 오른쪽 상세(넓게) — Jobs 화면 패턴.
  - 대시보드: 좌측 프로필 요약 카드 · 중앙 메인 피드 · 우측 보조 카드(선택).
- **모바일**: 단일 열, 카드는 좌우 보더·radius 제거하고 풀폭으로 쌓아도 된다.
- 카드 사이 간격은 `gap-2`~`gap-4`. 카드 내부 패딩 `p-4`(모바일)·`p-6`(데스크톱).

---

## 컬러 시스템

`app/globals.css`가 단일 출처. 아래 값은 shadcn 시맨틱 토큰으로 매핑된다.

### Light

| 역할 | 토큰 | 값 |
| --- | --- | --- |
| Primary (LinkedIn Blue) | `--primary` | `#0A66C2` |
| Primary hover/pressed | `--brand-hover` | `#004182` |
| Primary 연한 배경 | `--brand-subtle` | `#E8F3FF` |
| Background (웜 그레이) | `--background` | `#F4F2EE` |
| Card / Surface | `--card` | `#FFFFFF` |
| Text primary | `--foreground` | `#191919` |
| Text secondary | `--muted-foreground` | `#666666` |
| Border | `--border` | `#E0DFDC` |
| Hover 배경 | `--accent` | `#EBEBEB` |
| Success (매칭 높음) | `--success` | `#057642` |
| Warning | `--warning` | `#915907` |
| Destructive | `--destructive` | `#CC1016` |

### Dark

| 역할 | 값 |
| --- | --- |
| Primary | `#71B7FB` |
| Background | `#000000` |
| Card | `#1B1F23` |
| Text primary | `#E9E9E9` |
| Text secondary | `#B0B7BF` |
| Border | `#38434F` |

### 규칙

- 강조색은 **Primary 하나**. 링크·주요 CTA·선택 상태·포커스 링에만 쓴다.
- Success/Warning/Destructive는 **상태 표시 전용**(매칭 점수, 알림, 에러). 장식에 쓰지 않는다.
- 그라디언트·네온·파스텔 다색 조합 금지.
- 텍스트 대비 WCAG AA(4.5:1) 이상 유지.

---

## Typography

- 폰트: 시스템/뉴트럴 산세리프. 영문 `Inter`(현재 `next/font`), 한글은 `Pretendard` 권장(미도입 시 시스템 폰트 폴백).
- 굵기: 본문 400, 강조 600. 700 이상은 페이지 타이틀에만.

| 스타일 | Tailwind | 용도 |
| --- | --- | --- |
| Page title | `text-2xl font-semibold` | 페이지 제목 |
| Card title | `text-base font-semibold` / `text-lg` | 카드·공고 제목 |
| Body | `text-sm` | 본문 기본 (LinkedIn은 14px 본문) |
| Meta / Caption | `text-xs text-muted-foreground` | 회사명·위치·게시일 등 |

- 공고 제목처럼 클릭 가능한 텍스트는 hover 시 `underline` + primary 색.
- 긴 설명은 3~5줄에서 자르고 "더 보기"로 펼친다.

---

## Radius

| 대상 | 값 | Tailwind |
| --- | --- | --- |
| 카드·패널·입력 | 8px | `rounded-lg` |
| 이미지 썸네일·회사 로고 | 4px | `rounded-sm` |
| 버튼·칩·배지 | pill | `rounded-full` |
| 아바타 | 원형 | `rounded-full` |

---

## Shadow & Border

- 카드는 **얇은 보더(1px) 또는 아주 약한 그림자 하나**로 구분한다. 진한 그림자·blur 금지.
- 기본 카드: `border bg-card` (또는 `shadow-xs`).
- 드롭다운·팝오버만 `shadow-md` 수준 허용.

---

## Spacing

4의 배수: 4 · 8 · 12 · 16 · 24 · 32 · 48. Tailwind 기본 스케일(`1`·`2`·`3`·`4`·`6`·`8`·`12`)을 그대로 쓴다.

---

## 아이콘

- `lucide-react`만 사용. 크기 `size-4`(텍스트 옆) · `size-5`(버튼) · `size-6`(nav).
- 아이콘은 라벨을 보조한다. **아이콘 단독 버튼에는 `aria-label`** 필수.
- 이모지를 UI 아이콘 대신 쓰지 않는다.

---

## 컴포넌트 패턴

### 버튼

| 종류 | 스타일 |
| --- | --- |
| Primary | `rounded-full bg-primary text-primary-foreground`, hover `--brand-hover` |
| Secondary | `rounded-full border border-primary text-primary bg-transparent`, hover `bg-brand-subtle` |
| Tertiary / Text | `text-muted-foreground`, hover `bg-accent` |
| Icon | 원형, hover `bg-accent` |

- 라벨은 짧은 동사형: "지원하기", "저장", "이력서 업로드".
- 한 카드에 Primary 버튼은 하나.

### 카드

- 헤더(제목 + 메타) → 본문 → 하단 액션 순. 섹션 구분은 `border-t`.
- 카드 전체 클릭 영역이면 hover 시 `bg-accent/50` 정도만 변화.

### 공고 카드 (Job card)

- 회사 로고(정사각, `rounded-sm`) · 공고 제목(semibold, primary 링크) · 회사명 · 위치 · 메타(게시일, 매칭 점수).
- 매칭 점수/스킬 일치는 배지(`rounded-full`, `bg-brand-subtle text-primary` 또는 success)로 표시.

### 배지 / 칩

- 스킬·필터: `rounded-full border px-3 py-1 text-sm`. 선택 상태는 `bg-primary text-primary-foreground` 또는 진한 보더.

### 폼

- 라벨은 입력 위, `text-sm font-semibold`. 입력은 `rounded-lg border`, 포커스 시 primary 링.
- 에러는 입력 아래 `text-destructive text-xs` + 아이콘.

### Dialog / Sheet

- 데스크톱: 중앙 Dialog(`rounded-lg`, 헤더에 제목 + 닫기). 모바일: Bottom Sheet 허용.

---

## Empty / Loading State

- **Empty**: 작은 lucide 아이콘 + 한 줄 설명 + CTA 하나. 예) "아직 매칭된 공고가 없습니다" → [이력서 업로드].
- **Loading**: 실제 레이아웃 모양의 Skeleton(shadcn `Skeleton`). 전체 화면 스피너 지양.
- **Error**: 원인 한 줄 + 재시도 버튼.

---

## 디자인 체크리스트

- 강조색이 Primary 하나뿐인가?
- 웜 그레이 배경 + 흰 카드 구조인가?
- 정보 위계(제목 → 메타 → 본문)가 명확한가?
- 버튼이 pill, 카드가 8px radius인가?
- 그림자·장식이 과하지 않은가?
- 키보드 포커스·대비·`aria-label`이 갖춰졌는가?
- 모바일에서 단일 열로 자연스럽게 쌓이는가?

---

## AI 디자인 규칙

- LinkedIn 웹의 레이아웃·밀도·컬러 톤을 기준으로 한다. 로고·상표·고유 일러스트는 복제하지 않는다.
- 색은 `globals.css` 토큰만 쓴다. `slate-*`·`blue-*` 같은 Tailwind 원색 직접 사용 대신 시맨틱 토큰(`text-muted-foreground`, `bg-primary`)을 쓴다.
- shadcn 컴포넌트를 기본으로 쓰고, 톤 조정은 토큰과 wrapper로 한다(`components/ui/` 직접 수정 금지).
- 화려한 애니메이션·일러스트·이모지보다 깔끔한 타이포와 정렬을 우선한다.
