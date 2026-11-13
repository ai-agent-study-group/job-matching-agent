---
제목: "OpenAPI 스펙으로 FE용 TypeScript 타입 자동 생성 (#41)"
유형: "작업 메모"
설명: "티켓 #41에서 BE의 /api 응답 모델로 FE가 쓰는 TypeScript 타입을 만드는 흐름과 실행 방법을 정리합니다. BE 모델을 고치거나 FE에서 생성 타입을 쓸 때 보면 좋습니다."
관련문서:
    - "../structure/be.md"
    - "../structure/fe.md"
---

# OpenAPI 스펙으로 FE용 TypeScript 타입 자동 생성 (#41)

## 배경과 목적

[#41](https://github.com/ai-agent-study-group/job-matching-agent/issues/41)은 FE가 BE 응답 타입을 손으로 맞추지 않게 하는 작업입니다. 손으로 맞추면 BE 모델이 바뀌어도 FE는 모릅니다.

이제 BE 모델에서 TS 타입을 자동으로 만들고, 모델을 고쳐 커밋하면 훅이 타입을 다시 만듭니다.

## 주요 내용

### 흐름

`web/`에서 `npm run generate:types` 한 번이면 아래 1 · 2가 차례로 돕니다.

| 단계 | 하는 일 |
| --- | --- |
| 1. 스펙 추출 | `scripts/export_openapi.py`가 서버를 띄우지 않고 `app.openapi()`로 스펙을 만들어 `web/lib/api-types/openapi.json`에 저장 |
| 2. 타입 생성 | `openapi-typescript`가 `openapi.json`을 읽어 `web/lib/api-types/api.generated.ts`를 만듦 |
| 3. 자동 실행 | 아래 경로의 파일을 커밋하면 커밋 훅 `api-types`가 `generate:types`를 실행 |

생성 파일 두 개도 커밋합니다. FE는 BE를 실행하지 않고도 타입을 씁니다.

```ts
import type { components } from "@/lib/api-types/api.generated";

type JobPosting = components["schemas"]["JobPosting"];
```

지금은 `/api`에 `/health`만 있어서 `components["schemas"]`가 비어 있습니다. [#14](https://github.com/ai-agent-study-group/job-matching-agent/issues/14)가 응답 모델을 돌려주는 라우트를 붙이면 그 모델이 들어옵니다.

### 커밋 훅

| 항목 | 내용 |
| --- | --- |
| 감시 경로 | `src/main.py`, `src/adapter/inbound/api/`, `src/domain/` |
| 생성 파일이 바뀌면 | 커밋이 멈춤. 생성 파일 두 개를 `git add`하고 다시 커밋 (ruff format이 파일을 고쳤을 때와 같음) |
| 처음 한 번 | `cd web && npm ci`. 훅이 `web/node_modules`의 `openapi-typescript`를 씀 |

`/api`는 `domain/`의 모델을 그대로 돌려주므로 `domain/`도 감시합니다. BE 개발자도 `npm ci`를 한 번 해야 하는 이유입니다.

### TS 타입의 `?` 없애기

Pydantic은 기본값이 있는 필드를 "없어도 되는 필드"로 적습니다. 그래서 TS 타입에 `?`가 붙습니다. 그런데 BE 응답에는 이 필드가 항상 들어 있습니다.

`Profile` · `JobPosting`에 아래 설정을 넣어, 응답 스키마에서는 이 필드도 필수로 적게 했습니다.

```python
model_config = ConfigDict(json_schema_serialization_defaults_required=True)
```

| 필드 | 전 | 후 |
| --- | --- | --- |
| `JobPosting.url` | `url?: string \| null` | `url: string \| null` |
| `Profile.job_titles` | `job_titles?: string[]` | `job_titles: string[]` |

| 바뀌지 않는 것 | 바뀌는 것 |
| --- | --- |
| 기본값과 입력 검증 (`url` 없이 `JobPosting`을 만들 수 있음) | MCP `search_jobs` · `get_job`의 출력 스키마에서 `url` · `description`이 필수 키가 됨. 값은 여전히 `null`일 수 있음 |
| agent에 주는 출력 스키마 (입력용 스키마를 씀) | |

MCP 응답에는 원래 `url` · `description` 키가 `null`로라도 항상 들어 있어서, 실제 응답은 같습니다.

### 테스트

| 테스트 | 지키는 것 | 깨지면 |
| --- | --- | --- |
| `test/adapter/inbound/api/test_openapi.py` | 커밋된 `openapi.json`이 지금 `app.openapi()`와 같음 | 훅 없이 모델만 고쳐 커밋함. `web/`에서 `npm run generate:types` |

**테스트하지 않는 것:** `api.generated.ts`가 `openapi.json`대로 만들어졌는지. 두 파일은 `generate:types`가 같이 만듭니다.

## 결정 사항과 미정 사항

- 확정 ([#41 댓글](https://github.com/ai-agent-study-group/job-matching-agent/issues/41)):
    - 생성 파일 위치: `web/lib/api-types/`
    - 추출 스크립트 위치: 루트 `scripts/export_openapi.py`
    - `openapi-typescript`는 `web/`의 devDependency로 설치. 버전은 `package-lock.json`이 고정
- 범위 제외:
    - API 호출 코드 생성 (타입만 만듦)
    - CI에서 타입을 만드는 자동화 (로컬 스크립트와 커밋 훅으로 만듦)

## 다음 할 일

- [ ] #14 이후: FE 목 데이터 타입(`web/domain/`)을 생성 타입으로 바꾸기
