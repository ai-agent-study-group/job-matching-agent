---
title: 백엔드 API 연동
type: reference
description: 백엔드 API를 호출하는 화면을 만들 때 읽는다. 요청·응답 타입, 로딩·오류·빈 결과 처리, 이력서 매칭 흐름을 확인할 때 읽는다.
related:
  - ./AI_RULES.md
  - ./TESTING.md
---

# 백엔드 API 연동

백엔드 API를 호출하는 화면은 아래 규칙을 지킨다. 상세 코딩 규칙은 [AI_RULES.md](./AI_RULES.md), 수동 검증은 [TESTING.md](./TESTING.md).

## 타입

- 요청·응답·오류 형식은 백엔드 **OpenAPI 명세**를 단일 출처로 삼는다.
- 타입은 직접 쓰지 말고 생성물을 재사용한다 — `npm run generate:types` 가 `lib/api-types/api.generated.ts` 를 만든다.
- `any` 금지. 응답 타입을 명시한다.

## 로딩·오류·빈 결과

- 요청 중에는 **로딩 상태**를 표시하고, 같은 요청을 보내는 버튼의 **중복 클릭을 막는다**.
- 요청이 실패하면 **어느 작업이 실패했는지** 안내하고, **다시 시도**할 수 있게 한다.
- 성공 응답에 결과가 없으면 **빈 결과 안내**를 표시한다.
- 비동기 작업은 `try-catch` 또는 TanStack Query 의 에러 처리로 감싼다.

## 이력서 매칭 흐름

- **프로필 추출**(`#55` — `POST /api/profile`)과 **공고 검색**(`POST /api/search`)은 **각각** 로딩·오류 상태를 따로 표시한다.
- 한쪽 실패가 다른 쪽 상태를 가리지 않게 한다.
