---
제목: "Logfire로 agent · MCP 도구 호출 기록 (#49)"
유형: "작업 메모"
설명: "티켓 #49에서 FastAPI, Pydantic AI, FastMCP 도구와 출처 API 호출을 Logfire로 관찰하고, 이력서 원문이 기록되지 않게 한 방법을 정리합니다."
관련문서:
  - "../structure/devops.md"
  - "../structure/llm.md"
  - "../be/ticket-38.md"
---

# Logfire로 agent · MCP 도구 호출 기록 (#49)

## 배경과 목적

[#49](https://github.com/ai-agent-study-group/job-matching-agent/issues/49)은 서버의 agent와 MCP 도구가
어떤 순서로 실행되는지, 각 단계가 얼마나 걸리는지, LLM 호출의 토큰·비용 메타데이터를
Logfire에서 확인하는 작업이다.

관찰 대상은 두 경로다.

```text
Codex · ChatGPT · Claude ── MCP ──> /mcp ──> RegistryService ──> 출처 API
JMA 웹 앱                 ── API ──> /api/search ──> profile/search agent ──> MCP 도구
```
  
  - 외부 AI 앱은 `/mcp`의 데이터 도구를 직접 호출한다.
  - JMA 웹 앱은 `/api/search`로 이력서를 보내고, 서버의 Pydantic AI agent가 같은 MCP
    도구를 호출한다.
  - `domain/`, `port/`, `service/`는 Logfire를 알지 못한다. 관찰 설정은 조립부와
    inbound adapter에만 둔다.

## 구현

### 설정 위치

`src/observability.py`에 Logfire 설정을 모았다.

```python
def configure_logfire() -> None:
    logfire.configure(
        service_name="job-matching-agent",
        send_to_logfire="if-token-present",
    )
    logfire.instrument_pydantic_ai(include_content=False)
    logfire.instrument_httpx(capture_request_body=False, capture_response_body=False)
```

`src/main.py`은 FastAPI 앱을 만든 뒤 `configure_logfire()`와
`instrument_fastapi(app)`을 한 번씩 호출한다. stdio로 MCP 서버만 실행하는
`adapter.inbound.mcp.server`도 같은 설정을 실행한다. 따라서 API와 독립 MCP 서버 모두
같은 프로젝트 이름으로 trace를 내보낸다.

| 계측 대상 | 설정 | 확인하는 것 |
| --- | --- | --- |
| FastAPI | `instrument_fastapi(app)` | 요청 경로, 상태, 전체 시간 |
| Pydantic AI | `instrument_pydantic_ai(include_content=False)` | agent 실행 단계, 모델 호출 시간, 토큰·비용 메타데이터 |
| MCP | FastMCP 4의 기본 OpenTelemetry span | 도구 이름, 인자/결과 span, 시간, 오류 |
| 출처 API | `instrument_httpx(...)` | HTTP 호출 시간, 상태, 오류 |

FastMCP 4는 `mcp>=2`를 사용한다. 이 버전은 span과 trace context를 기본으로 만들기 때문에
`logfire.instrument_mcp()`을 추가로 호출하지 않는다. FastMCP 4에서 그 호출은 불필요한
경고만 남긴다.

### 개인정보 보호

이력서와 공고 본문은 관찰 데이터로 보내지 않는다.

| 위험 지점 | 보호 방식 |
| --- | --- |
| `/api/search`의 `resume_text` | FastAPI `request_attributes_mapper`가 검증된 요청 인자를 빈 값으로 교체 |
| profile/search agent의 입력·출력 | `include_content=False`로 메시지 본문 제외 |
| 출처 API 요청·응답 | `capture_request_body=False`, `capture_response_body=False` |

이 설정은 호출 순서·시간·상태·토큰 같은 운영 정보는 남기지만, 이력서 원문과 공고 본문은
남기지 않는다. 새로 직접 `logfire.info()`를 쓸 때도 이력서처럼 민감한 값을 문자열에
직접 넣지 않는다.

## 토큰 없이 로컬에서 확인하기

`LOGFIRE_TOKEN`이 없어도 애플리케이션과 테스트는 실행된다.
`send_to_logfire="if-token-present"` 때문에 토큰이 없을 때 원격 Logfire로 데이터를 보내지
않는다. 테스트는 가짜 출처와 Pydantic AI 테스트 모델을 사용하므로 LLM API를 호출하지 않고
**0 토큰**이다.

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

`test/test_observability.py`는 다음 안전장치를 확인한다.

- 토큰이 없어도 `if-token-present` 설정으로 초기화되는지
- agent 본문 기록이 꺼져 있는지
- HTTP 요청·응답 본문 기록이 꺼져 있는지
- FastAPI request span에 `resume_text`가 들어가지 않는지

## 실제 Logfire에서 보기

Logfire 프로젝트의 write token은 저장소에 넣지 않고 로컬 `.env` 또는 배포 환경의 secret에만
둔다.

```env
LOGFIRE_TOKEN=<Logfire write token>
LLM_MODEL=openai:gpt-4.1-mini
OPENAI_API_KEY=<API key>
```

```bash
uv run --env-file .env uvicorn main:app --reload
curl http://localhost:8000/health
```

`/health`는 LLM을 호출하지 않으므로 FastAPI trace만 생기며 0 토큰이다. 실제 agent와
MCP 흐름은 `/api/search` 요청으로 확인한다. 이 경로는 서버의 LLM API 키를 쓰므로 모델
토큰 비용이 발생한다.

Codex·ChatGPT·Claude 같은 외부 클라이언트가 `/mcp`를 호출하면 서버의 MCP 도구 span과
시간은 볼 수 있다. 하지만 그 클라이언트 내부 LLM의 토큰·시간은 이 서버가 관찰할 수 없다.
클라이언트도 같은 Logfire 프로젝트로 계측했을 때만 하나의 분산 trace로 연결된다.

## 검증 결과

로컬에서 아래 검사를 실행했다.

```text
52 passed
ruff check .              All checks passed!
ruff format --check .     69 files already formatted
```

Logfire write token을 제공하지 않았으므로 실제 원격 Live 화면 전송은 검증하지 않았다.
토큰을 가진 환경에서 `/health`와 `/api/search`를 각각 한 번 호출해 FastAPI trace와
agent → MCP → 출처 API의 하위 span을 확인하면 완료 조건을 검증할 수 있다.

## 참고

- [Logfire FastAPI 계측](https://pydantic.dev/docs/logfire/integrations/web-frameworks/fastapi/)
- [Logfire Pydantic AI 계측](https://pydantic.dev/docs/logfire/integrations/llms/pydanticai/)
- [Logfire MCP 및 FastMCP 4](https://pydantic.dev/docs/logfire/integrations/llms/mcp/)
