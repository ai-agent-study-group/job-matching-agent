# job-matching-agent

등록한 채용 사이트에서 공고를 검색·추출하고, 내 이력과 요건 단위로 매칭해 근거와 평가 결과를 보여주는 에이전트.

## 구현 범위와 흐름

검색할 사이트 목록 설정 → 내 이력 직접 등록 → 검색·추출 → 비교·매칭 → 평가 → 결과 확인.

- **PoC:** 사이트 목록과 이력을 미리 등록한 뒤 검색부터 평가까지 사람 개입 없이 이어지는 파이프라인을 실행하고, 화면에서 결과를 확인합니다. 이력 등록 형식(JSON 파일 또는 입력 폼)과 사이트 목록 등록 방식은 미정입니다.
- **공고 입력:** PoC에서는 매칭 agent가 공고 원문을 바로 읽습니다. JD 사전 구조화를 별도 단계로 둘지는 추후 결정합니다.
- **추후:** 이력서 업로드·파싱, 대화로 이력 보충. 파싱은 Markdown 변환 + LLM 구조화가 후보입니다.
- **PoC 제외:** Gmail 등 구인 사이트 알림 메일 수집.

범위와 미결 질문은 [10월 20일 회의 안건](docs/meetings/2026-10-20.md)에 정리합니다. 도메인 항목, 역할 구분과 담당자, 구현 비교 방식은 회의에서 확정합니다.

## 디렉터리와 작업 범위

| 경로 | 내용 | 담당 상태 |
| --- | --- | --- |
| `src/domain/` | 모든 층이 같이 쓰는 데이터 형식 (Profile · SearchQuery · JobPosting · JD · MatchResult) | - |
| `src/port/` | 코어와 어댑터 사이 약속. `inbound` = 서비스 포트, `outbound` = 공고 출처 · 저장소 | - |
| `src/service/` | 서비스 포트 구현 · 도구 / 서비스 로직 | - |
| `src/adapter/inbound/` | `api`(FE용 /api) · `mcp`(MCP 서버) · `agent`(pydantic-ai) | - |
| `src/adapter/outbound/` | 공고 출처(Greenhouse · 연방고용청 API, 스크래퍼는 추후) · 저장소(추후) | - |
| `src/main.py` | 조립: 어댑터를 service에 연결하고 /api와 /mcp를 한 앱에 올림 | - |
| `test/` | `src/`와 같은 구조의 백엔드 테스트 | - |
| `web/` | 사이트 목록 설정, 이력 등록, 결과·근거 확인 | - |
| `infra/` | 배포, CI | - |
| `eval/` | 평가셋, 정답 라벨 | - |
| `docs/` | 작업 문서, 공통 안내, 날짜별 회의 기록 | 전원 |

BE는 루트의 Python 프로젝트 하나(`pyproject.toml`, `src/`), FE는 `web/`입니다. 현재 API는 `/health`만 구현되어 있습니다. 위 표는 작업 범위이며 기능 구현 완료를 뜻하지 않습니다.
`src/`는 헥사고날(포트 · 어댑터) 구조입니다. DB, 실행 프로세스와 작업 전달 방식은 미정입니다. 기존 BE1·BE2·LLM1·LLM2 구분과 새 작업의 관계는 [프로젝트 역할](docs/TEAM.md)에서 확인합니다.

## 로컬 실행

필요: [uv](https://docs.astral.sh/uv/)

```bash
uv sync                         # BE 의존성 + 개발 도구 설치 (.venv 자동 생성)
uv run uvicorn main:app --reload
# http://localhost:8000/health
```

테스트, 린트:

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

의존성 추가: `uv add <라이브러리>` (개발 도구는 `uv add --dev`)

`src/` 바로 아래에 패키지(폴더)를 새로 만들면 `pyproject.toml`의 `module-name` 목록에도 추가. `main.py`는 파일이라 목록에 넣지 않음.

## 브랜치와 PR

[CONTRIBUTING.md](CONTRIBUTING.md) 참고.

## 문서와 회의

정기 모임은 기본적으로 **매주 화요일 18:00, Discord**에서 진행합니다.

[프로젝트 역할](docs/TEAM.md) · [현재 구조와 기술](docs/STRUCTURE.md) · [회의 기록](docs/meetings/README.md) · [문서 작성 안내](docs/GITHUB_GUIDE.md)

직군별 작업 공간: [기획](docs/po/README.md) · [프론트엔드](docs/fe/README.md) · [백엔드](docs/be/README.md) · [인공지능·언어 모델](docs/ai-llm/README.md) · [데이터 수집](docs/data/README.md) · [인프라·개발 운영](docs/infra/README.md).

Markdown 문서와 문서용 이미지만 변경하면 PR은 선택 사항입니다. 코드·사이트 화면·설정 변경은 [기여 규칙](CONTRIBUTING.md)의 PR 절차를 따릅니다.

### 문서 로컬 미리보기

이 프로젝트 루트(`job-matching-agent/`)에서 Node.js 20 이상으로 실행합니다.

```bash
npm ci
npm run docs:dev
```

[http://localhost:4173](http://localhost:4173)에서 문서를 읽고 제목을 검색할 수 있습니다. 파일을 저장하면 자동 갱신됩니다.
다른 문서 서버가 같은 포트를 사용 중이면 `DOCS_PORT=4175 npm run docs:dev`로 실행합니다.
이 npm 설정은 문서 도구용이며 Python 백엔드와 `web/`의 개발 환경은 별도로 관리합니다.

### 공개 문서 사이트

GitHub 저장소의 Settings → Pages에서 **Deploy from a branch → main → /docs**를 선택합니다.
배포 후 [문서 사이트](https://ai-agent-study-group.github.io/job-matching-agent/)에서 같은 화면을 사용할 수 있습니다.
새 Markdown 문서는 직군별 메뉴에 자동으로 추가되며, 작성·수정 버튼은 job-matching-agent 저장소로 연결됩니다.
