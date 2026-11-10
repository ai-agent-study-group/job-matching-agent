---
제목: "검색 agent 최소판 (#14)"
유형: "작업 메모"
설명: "티켓 #14에서 만드는 검색 agent가 헥사고날 구조의 어디에 있고, Profile을 이용해 MCP 도구로 채용공고를 검색한 뒤 JobPosting 목록을 반환하는 과정을 정리합니다."
관련문서:
  - "../structure/llm.md"
  - "../structure/be.md"
---

# 검색 agent 최소판 (#14)

## 배경과 목적

[#14](https://github.com/ai-agent-study-group/job-matching-agent/issues/14)은 #13에서 추출한 `Profile`을 이용해 채용공고를 검색하는 작업입니다.

검색 agent는 `Profile`의 직무명과 희망 근무지를 바탕으로 적절한 채용공고 출처를 선택하고, MCP 도구를 호출하여 검색 결과를 가져옵니다.

출처별 검색 파라미터 형식은 서로 다르므로, 검색 agent가 `get_usage()`를 통해 필요한 파라미터를 확인합니다.

## 주요 내용

### 전체 그림

검색 agent는 헥사고날 구조에서 `adapter/inbound/agent/search.py`에 위치합니다.

호출 흐름은 다음과 같습니다.

1. `create_search_agent(model, mcp_toolset)`으로 검색 agent를 생성합니다.
2. `agent.run(profile.model_dump_json())`으로 검색을 실행합니다.
3. LLM이 `list_sources()`를 호출하여 사용 가능한 출처를 확인합니다.
4. `get_usage(source)`로 해당 출처의 검색 파라미터 형식을 확인합니다.
5. `search_jobs(source, params)`를 호출하여 채용공고를 검색합니다.
6. 검색 오류가 발생하면 LLM이 파라미터를 수정하여 다시 호출할 수 있습니다.
7. Agent 실행 후 `extract_jobs(result)`로 검색 결과를 추출하고 중복을 제거합니다.
8. 최종적으로 `list[JobPosting]`을 반환합니다.

### 만들 파일

| 파일 | 하는 일 |
| --- | --- |
| `src/adapter/inbound/agent/search.py` | `SEARCH_PROMPT`, `create_search_agent()`, `extract_jobs()` |
| `src/adapter/inbound/api/route.py` | Profile Agent 및 Search Agent 호출, 검색 결과 반환 |
| `src/adapter/inbound/api/dto.py` | 검색 요청 DTO 및 이력서 입력 검증 |
| `test/adapter/inbound/agent/test_search.py` | Search Agent 동작 테스트 |
| `test/adapter/inbound/api/test_route.py` | FastAPI → Search Agent → MCP 통합 테스트 |

### Search Agent 생성

`create_search_agent()`는 모델 이름과 MCP Toolset을 인자로 받아 Pydantic AI의 `Agent` 객체를 생성합니다.

```python
def create_search_agent(model: str, mcp_toolset: MCPToolset) -> Agent:
    return Agent(
        model,
        toolsets=[mcp_toolset.filtered(lambda ctx, tool: tool.name != "get_job")],
        instructions=SEARCH_PROMPT,
        output_type=str,
        retries={"tools": 5},
    )
```

- `model`: 사용할 LLM 모델
- `mcp_toolset`: 검색에 필요한 MCP 도구
- `instructions`: 검색 순서를 설명하는 지시문
- `output_type=str`: Agent의 최종 응답 형식
- `retries={"tools": 5}`: 도구 검증 및 재시도 요청을 최대 5회 허용

`get_job`은 상세 공고 조회 도구이므로 검색 agent에서는 제외합니다.

### MCP 도구 호출

| 도구 | 역할 |
| --- | --- |
| `list_sources()` | 사용 가능한 채용공고 출처 조회 |
| `get_usage(source)` | 선택한 출처의 검색 파라미터 JSON Schema 조회 |
| `search_jobs(source, params)` | 실제 채용공고 검색 |

검색 agent는 `SEARCH_PROMPT`의 지시에 따라 이 도구들을 사용합니다.

검색 파라미터가 잘못된 경우 LLM이 오류 내용을 참고해 수정한 뒤 재호출할 수 있습니다.

검색 결과를 좁히기 위한 추가 검색과 `retries={"tools": 5}`에 따른 도구 재시도는 서로 다른 개념입니다.

### 검색 결과 추출

`extract_jobs()`는 `search.py`에 정의된 일반 Python 함수입니다.

Agent가 자동으로 호출하는 도구가 아니라, `route.py`에서 Agent 실행 후 직접 호출합니다.

```python
result = await search_agent.run(profile.model_dump_json())
return extract_jobs(result)
```

`extract_jobs()`는 다음 작업을 수행합니다.

1. Agent 실행 기록에서 `search_jobs`의 `ToolReturnPart`를 찾습니다.
2. 반환된 항목을 `JobPosting`으로 검증합니다.
3. `(source, id)`를 기준으로 중복을 제거합니다.
4. 최종 `list[JobPosting]`을 반환합니다.

### LLM이 읽는 것

| 쓰는 곳 | LLM에게 보이는 것 |
| --- | --- |
| `SEARCH_PROMPT` | 검색 순서와 도구 사용 지시문 |
| `agent.run(...)` | JSON으로 변환된 Profile |
| MCP 도구 설명 | 도구의 기능과 파라미터 |
| `get_usage()` 반환값 | 출처별 검색 파라미터 JSON Schema |

`extract_jobs()`의 docstring은 LLM에게 전달되지 않습니다.

## 결정 사항과 미정 사항

- 확정:
  - 검색 agent는 `Profile`을 입력으로 받음
  - MCP 도구를 이용하여 채용공고 검색
  - 출처별 검색 조건은 `get_usage()`를 통해 확인
  - `get_job` 도구는 검색 agent에서 제외
  - Agent 최종 출력은 `str`
  - `extract_jobs()`가 `JobPosting` 목록을 추출하고 중복 제거
  - FastAPI `/api/search`에서 Profile Agent와 Search Agent를 연결
  - `FunctionModel` 기반 통합 테스트 사용

- 향후 검토:
  - 검색 결과의 최대 개수 및 정렬 정책
  - 검색 조건을 추가로 좁히는 기준
  - 여러 채용공고 출처를 동시에 검색하는 전략

## 다음 할 일

- [x] Search Agent 생성
- [x] MCP 도구 연결
- [x] FastAPI 검색 API 연결
- [x] 검색 결과 추출 및 중복 제거
- [x] 통합 테스트 작성
- [ ] README.md에 LLM 환경변수 설정 방법 추가
- [ ] GitHub Actions 전체 검사 통과 확인
- [ ] #51: 공고 정리 Agent 구현 (`get_job` → 구조화된 JD 추출)