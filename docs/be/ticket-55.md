---
제목: "/api를 프로필 추출과 공고 검색으로 나누기 (#55)"
유형: "작업 메모"
설명: "티켓 #55에서 /api/search 하나를 /api/profile과 /api/search로 나누고, agent가 실패하면 JSON 에러를 돌려주게 한 내용입니다."
관련문서:
    - "../ai-llm/ticket-14.md"
    - "../structure/be.md"
---

# /api를 프로필 추출과 공고 검색으로 나누기 (#55)

## 배경과 목적

[#14](../ai-llm/ticket-14.md)의 `POST /api/search`는 이력서 텍스트를 받아, 한 요청 안에서 프로필 agent와 검색 agent를 차례로 돌렸습니다. 그래서 두 가지가 안 됐습니다.

- 사용자가 추출된 직무명과 희망 근무지를 확인하거나 고친 뒤 검색하기. [현재 구조와 기술](../STRUCTURE.md)의 JMA 앱 흐름에 있는 단계입니다.
- 실패했을 때 어느 단계에서 실패했는지 알기. 실패하면 평문 500(`Internal Server Error`)만 왔습니다.

## 바뀐 경로

| 경로 | 받는 것 | 돌려주는 것 | 실패하면 |
| --- | --- | --- | --- |
| `POST /api/profile` | `{"resume_text": "..."}` (이력서 텍스트) | `Profile` (`job_titles`, `locations`) | 502 · 503 · 504 `{"detail": "Profile extraction failed. <원인>"}` |
| `POST /api/search` | `Profile` | 공고 목록 (`JobPosting[]`) | 502 · 503 · 504 `{"detail": "Job search failed. <원인>"}` |

JMA 앱은 `/api/profile`의 응답을 화면에 보여 주고, 사용자가 고친 프로필을 그대로 `/api/search`에 보냅니다. `/api/search`의 요청 본문은 도메인 `Profile`을 그대로 씁니다.

`/api/profile`은 #44에서 이력서 파일(PDF · DOCX)을 받도록 바뀝니다. 그때까지는 이력서 텍스트를 JSON으로 받습니다. 프로필 agent는 긴 이력서에서 직무명과 근무지를 뽑아내는 일을 해서, 사용자가 직무명과 근무지를 이미 안다면 agent를 거치지 않고 FE 프로필 화면에서 바로 적은 뒤 `/api/search`를 부르면 됩니다. 그래서 텍스트를 받는 경로는 따로 두지 않습니다.

JSON 문자열 안에서는 줄바꿈과 따옴표를 `\n`, `\"`로 적어야 합니다. Swagger나 curl에 여러 줄 이력서를 그대로 붙여 넣으면 422(`json_invalid`)가 납니다. FE는 `JSON.stringify`가 알아서 바꿔 줘서 상관없습니다.

## 실패 처리

agent를 돌리다 pydantic-ai가 `AgentRunError`를 내면 예외 종류에 따라 상태 코드를 고릅니다(`agent_error`). LLM과 출처 API는 이 서버 바깥의 서비스라서 5xx 중 게이트웨이 계열을 씁니다.

| 코드 | 경우 | 예외 | FE가 할 일 |
| --- | --- | --- | --- |
| 503 | LLM 사용량 제한, 과부하 | `ModelRateLimitError`, `ModelUnavailableError`(과부하 `ModelOverloadedError` 포함) | 잠시 후 다시 시도 |
| 504 | LLM 응답 시간 초과 | `ModelTimeoutError`, `ModelRequestTimeout` | 잠시 후 다시 시도 |
| 502 | 그 밖의 agent 실패 | 나머지 `AgentRunError` | 실패 안내 |

사용량 제한, 과부하, 시간 초과는 자주 나고 잠깐 뒤에 다시 하면 대부분 되는 오류라 따로 나눴습니다. 502가 나는 경우는 경로마다 다릅니다.

| 경로 | 502가 나는 경우 |
| --- | --- |
| `/api/profile` | 인증 오류 같은 그 밖의 LLM 호출 실패, 또는 LLM이 재시도 후에도 `Profile` 형식에 맞는 답을 못 냄 |
| `/api/search` | 그 밖의 LLM 호출 실패, 또는 검색 도구가 재시도 한도(5번)를 넘게 실패함 |

검색 도구가 실패하는 원인은 출처 API 장애만이 아닙니다. LLM이 틀린 검색 인자를 계속 넣거나, 결과가 너무 많은데 조건을 좁히지 않아도 같은 오류로 끝납니다. 도구 오류는 MCP를 지나며 문자열로 LLM에게 전달되기 때문에, 라우트에서는 원인을 구분하지 않습니다. 원인은 서버 로그와 Logfire(#49)에서 봅니다.

- 응답의 `detail`은 "실패한 단계. 원인" 꼴입니다(예: `Profile extraction failed. The LLM is rate limited or overloaded. Try again later`). 원인 문장은 상태 코드마다 정해 둔 것(`AGENT_ERROR_REASONS`)이고, Swagger의 응답 설명도 같은 문장을 씁니다.
- LLM 제공자가 보낸 오류 원문은 응답에 넣지 않고 서버 로그(`agent_error`의 `logger.error`, traceback 포함)에만 남깁니다. 제공자 응답 본문, 모델 이름, 요청 ID 같은 내부 정보가 섞여 있기 때문입니다.
- 그 밖의 예외는 코드 버그로 보고 지금처럼 500으로 둡니다.

## Swagger

- 두 경로 모두 `responses`에 502 · 503 · 504 응답 모양(`ErrorDTO`)과 예시를 적었습니다. FE용 TS 타입에도 에러 모양이 생깁니다.
- `/api/search` 요청에는 예시를 붙이지 않았습니다. 도메인 `Profile`에 예시를 넣으면 프로필 agent가 받는 출력 스키마에도 들어가서, 이력서에 없는 근무지를 예시대로 채울 수 있습니다. Swagger에서는 `/api/profile` 응답을 복사해 넣으면 됩니다.
- `Profile`이 응답과 요청에 모두 쓰여서 스펙에는 `Profile-Output`과 `Profile-Input` 두 이름으로 나옵니다. 응답 쪽은 필드가 항상 있고(#41의 설정), 요청 쪽은 빈 목록이면 필드를 생략해도 됩니다. 그래서 응답 타입을 그대로 요청에 넣을 수 있습니다.

## 파일 구성

| 파일 | 바뀐 것 |
| --- | --- |
| `adapter/inbound/api/route.py` | `/api/profile` 추가, `/api/search`가 `Profile`을 받음 |
| `adapter/inbound/api/error.py` | agent 실패를 로그에 남기고 502 · 503 · 504로 바꿈(`agent_error`), 같은 내용을 Swagger에 적음(`agent_errors`). 새 파일 |
| `adapter/inbound/api/dto.py` | `SearchRequestDTO`를 `ProfileRequestDTO`(`{"resume_text": ...}`)로 바꾸고 `ErrorDTO` 추가. `ProfileRequestDTO`는 #44에서 파일 업로드로 바뀔 때 지움 |
| `web/lib/api-types/` | 스펙과 TS 타입 다시 생성 |

## 테스트

| 테스트 | 지키는 것 |
| --- | --- |
| `test_profile_returns_profile_from_resume` | 이력서를 보내면 프로필 agent의 결과가 그대로 옴 |
| `test_profile_rejects_blank_resume` | 비어 있거나 공백뿐인 이력서는 422 |
| `test_profile_agent_failure_maps_to_status` | 프로필 agent의 오류 종류마다 503 · 504 · 502가 나오고, 본문은 `Profile extraction failed` |
| `test_search_returns_postings_from_search_jobs` | 프로필을 보내면 `search_jobs`가 찾은 공고가 옴 |
| `test_search_agent_failure_maps_to_status` | 검색 agent의 사용량 제한은 503, 도구 재시도 소진은 502이고, 본문은 `Job search failed` |
