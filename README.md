# job-matching-agent

구인 사이트 알림으로 들어온 공고의 JD를 수집해, 저장된 이력과 요건 단위로 매칭도를 분석하는 에이전트.

## 흐름

1. **ingest**: 알림 메일에서 회사·포지션·링크 추출, 중복 제거
2. **scraper**: 링크 또는 회사 커리어 사이트에서 JD 확보 (ATS 어댑터 + Playwright 범용 추출)
3. **llm**: JD 구조화, 이력과 요건별 매칭 (충족 여부 + 근거 출처)
4. **api**: 공고·이력·매칭 결과 저장과 조회 (FastAPI)
5. **web**: 공고 목록, 매칭 근거 대시보드, 이력 편집

BE는 루트의 Python 프로젝트 하나 (`pyproject.toml`, `src/`), FE는 `web/`.
BE 모듈은 한 패키지에 두고 실행만 프로세스별로 나눔 (API 서버, 워커). DB, 프로세스 간 작업 전달 방식은 진행하면서 결정.

## 디렉터리와 담당

| 경로 | 내용 | 담당 |
|---|---|---|
| `src/ingest` | 알림 수집, 스케줄러, 중복 제거 | BE1 |
| `src/scraper` | ATS 어댑터, 스크래핑 워커 | BE2 |
| `src/llm` | JD 구조화, 매칭, 점수 산정 | LLM1, LLM2 |
| `src/api` | REST API, DB | BE1 |
| `src/schemas` | JD, 이력, 매칭 결과 스키마 (pydantic) | 전원 합의 |
| `tests` | BE 테스트 | 각 담당 |
| `web` | 프론트엔드 | FE |
| `infra` | 배포, CI | DevOps |
| `eval` | 평가셋, 정답 라벨 | LLM2, PO |

PO: 매칭 기준 정의, 정답 라벨링, 우선순위.

## 로컬 실행

필요: [uv](https://docs.astral.sh/uv/)

```bash
uv sync                         # BE 의존성 + 개발 도구 설치 (.venv 자동 생성)
uv run uvicorn api.main:app --reload
# http://localhost:8000/health
```

테스트, 린트:

```bash
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

의존성 추가: `uv add <라이브러리>` (개발 도구는 `uv add --dev`)

`src/` 아래에 모듈을 새로 만들면 `pyproject.toml`의 `module-name` 목록에도 추가.

## 브랜치와 PR

[CONTRIBUTING.md](CONTRIBUTING.md) 참고.
