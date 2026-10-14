# job-matching-agent

업로드한 이력서와 채용공고 JD를 요건 단위로 비교하고, 매칭된 공고 목록을 제공하는 에이전트 스터디입니다.

## 스터디 문서와 모임

**정기 모임: 매주 화요일 18:00 (Europe/Berlin).** 첫 회의: 2026-10-13.

- [첫 회의 요약](docs/meetings/2026-10-13.md)
- [Phase 1·2 개발 범위](docs/PROJECT_PLAN.md)
- [역할과 협업](docs/TEAM.md) · [현재 구조](docs/STRUCTURE.md)
- [이력서·JD 데이터](docs/DATA.md) · [평가 논의](docs/EVALUATION.md)
- [날짜별 회의 기록](docs/meetings/README.md) · [문서 작성·미리보기](docs/GITHUB_GUIDE.md)

Phase 1은 첫 1개월 동안 이력서 업로드 → JD 수집·분석 → 매칭 공고 목록을 연결하는 범위 초안입니다.
챗봇·JSON 프로필 입력과 공고별 이력서 최적화·다운로드는 Phase 2 확장으로 구분합니다.
우선 사이트·수집 주기·점수 산식·담당·완료 기준은 미정입니다.

문서 사이트 로컬 미리보기 (프로젝트 루트, Node.js 20 이상):

```bash
npm install
npm run docs:dev
# http://localhost:4174
```

파일 저장 시 자동 갱신됩니다. Python 서버와 Next.js 앱의 실행과는 별개입니다.
문서 사이트는 GitHub Pages의 `main → /docs` 배포로 공개할 수 있습니다. 실제 배포·푸시는 수행하지 않았습니다.

현재 Python 서버는 `/health` 기본 API이며, `web/`은 규칙 기반 이력서 매칭 데모입니다.
아래 흐름·역할 구분은 기존 저장소의 개발 방향이며, 구현 완료나 개인별 배정 확인을 뜻하지 않습니다.

## 흐름

1. **입력·수집**: 이력서 업로드·정보 추출과 공고 수집 실행. 기존 메일 수집 계획의 우선순위는 추가 논의
2. **scraper**: 링크 또는 회사 커리어 사이트에서 JD 확보 (ATS 어댑터 + Playwright 범용 추출)
3. **llm**: JD 필수·우대·업무 구조화, 이력과 요건별 매칭·점수·근거 (산식 미정)
4. **api**: 공고·이력·매칭 결과 저장과 조회 (FastAPI)
5. **web**: 이력서 업로드, 매칭 공고 목록·근거 표시. 입력 다변화는 Phase 2

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
