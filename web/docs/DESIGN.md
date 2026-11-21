고---
title: 디자인 시스템
type: reference
description: 화면 UI를 만들 때 읽는다. 컬러, 타이포그래피, radius, spacing, 아이콘, 애니메이션, 버튼, Bottom Sheet, Empty State 등 디자인 토큰과 규칙을 찾을 때 읽는다.
related:
    - ./AI_RULES.md
    - ./FEATURE.md
---

# 디자인 시스템

## 디자인 목표

이 앱은 **"디자이너 없이도 App Store 수준의 완성도"**를 목표로 한다.

Material Design 느낌을 최소화하고, Apple iOS 앱처럼 심플하면서도 부드러운 인터랙션을 제공한다.

사용자가 앱을 열었을 때 "재미있다", "만지는 맛이 있다", "계속 눌러보고 싶다"는 느낌을 받을 수 있어야 한다.

---

## 디자인 키워드

- iMessage Sticker
- Apple Photos Markup
- Apple Photos Editor
- Apple Sticker Pack
- LINE Sticker
- 카카오 이모티콘
- Instagram Story Editor
- CapCut
- Canva
- Notion Mobile
- Arc Browser

핵심 키워드

- Playful
- Friendly
- Modern
- Minimal
- Soft
- Fast
- Smooth

---

## 디자인 원칙

### 1. 아이콘과 이미지를 적극 활용한다.

텍스트보다 아이콘을 우선한다.

좋은 예

✂️ Crop

😊 Sticker

💬 Bubble

🎨 Color

📤 Export

나쁜 예

"이력서 다시 업로드하기"

"매칭 공고 전체 보기"

처럼 긴 텍스트 버튼을 만들지 않는다.

가능하면 아이콘 + 짧은 텍스트를 사용한다.

---

### 2. Floating UI

Bottom Navigation보다

Floating Toolbar를 우선한다.

예시

Apple Photos

CapCut

Instagram Story

처럼

필요한 순간에만 툴이 나타난다.

---

## 컬러 시스템

### Primary

White

#FFFFFF

---

### Background

#FAFAFA

---

### Surface

#FFFFFF

---

### Text

Primary

#111111

Secondary

#666666

Disabled

#BBBBBB

---

### Accent

Yellow

#FFD54F

Pink

#FF5C8D

Blue

#5B8CFF

Green

#30D158

Red

#FF453A

Accent Color는 한 화면에 하나만 사용한다.

---

## Typography

Google Fonts 사용

추천

- Pretendard
- Inter
- SF Pro (가능한 경우)
- Noto Sans

텍스트 스타일

Heading

24~32

Title

18~22

Body

16

Caption

13~14

---

## Radius

Small

8

Medium

16

Large

24

Pill

999

---

## Shadow

강한 그림자는 사용하지 않는다.

Soft Shadow만 사용한다.

Blur를 많이 사용한다.

---

## Spacing

4

8

12

16

20

24

32

48

모든 간격은 4의 배수를 사용한다.

---

## 아이콘

Material Icons를 기본으로 사용하지 않는다.

가능하면 아래 아이콘을 우선 사용한다.

- HugeIcons
- Lucide Icons
- Cupertino Icons
- Remix Icons
- Phosphor Icons

아이콘 크기

20

24

28

32

---

## 이미지 에셋

무료 에셋을 적극 활용한다.

추천 사이트

- Icons8
- SVG Repo
- Lucide
- Phosphor Icons
- OpenMoji
- Storyset
- unDraw
- LottieFiles
- Lordicon
- ManyPixels

사용 원칙

- SVG 우선
- PNG 최소화
- WebP 적극 사용

---

## 일러스트

빈 화면은

텍스트만 보여주지 않는다.

항상

- 귀여운 아이콘
- 작은 일러스트
- 미니 캐릭터

등을 함께 사용한다.

---

## 애니메이션

모든 화면 전환은 애니메이션을 사용한다.

추천

Fade

Scale

Hero

Shared Transition

Slide

Bottom Sheet

Elastic

Spring Animation

사용자가 버튼을 누르면

Haptic Feedback을 적극 사용한다.

---

## 인터랙션

드래그

핀치 줌

회전

더블탭 확대

롱프레스

스와이프

모두 자연스럽게 동작해야 한다.

---

## 버튼

Primary

Accent Color

Secondary

Outlined

Icon Button

Floating Button

Text Button

버튼은 최대한 둥글게 만든다.

---

## Bottom Sheet

Dialog보다 Bottom Sheet를 우선한다.

텍스트 입력

색상 선택

템플릿 선택

폰트 선택

모두 Bottom Sheet를 사용한다.

---

## Empty State

빈 화면을 만들지 않는다.

항상

아이콘

짧은 설명

CTA 버튼

를 함께 제공한다.

---

## 디자인 체크리스트

모든 화면은 아래 항목을 만족해야 한다.

- 아이콘이 충분한가?
- 이미지가 충분한가?
- 텍스트가 너무 많지 않은가?
- 애니메이션이 자연스러운가?
- 터치 피드백이 있는가?
- Empty State가 예쁜가?
- Material Design 느낌이 강하지 않은가?
- iOS 감성이 느껴지는가?
- 한 손으로 사용하기 편한가?
- 10초 안에 원하는 기능을 찾을 수 있는가?

---

## AI 디자인 규칙

AI는 UI를 생성할 때 아래 원칙을 반드시 따른다.

- Material Design 기본 UI를 그대로 사용하지 않는다.
- 아이콘과 이미지를 적극 활용한다.
- SVG 아이콘을 우선 사용한다.
- 일러스트와 Empty State를 적극 활용한다.
- 부드러운 애니메이션을 기본으로 한다.
- 버튼보다 제스처를 우선한다.
- 텍스트보다 시각적 요소를 우선한다.
- 웹(CSS/Tailwind)에서 무료로 구현 가능한 디자인을 우선한다.
- App Store 수준의 완성도를 목표로 한다.
