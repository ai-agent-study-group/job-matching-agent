## Railway 백엔드 배포 가이드 및 작업 기록 — Issue #48

> 이 문서는 당시의 배포 기록입니다. 현재 저장소 구조에서는 백엔드 Root Directory가 `/backend`이며 Dockerfile도 그 안에 있습니다. 최신 실행 방법은 저장소 README를 참고하세요.

- **프로젝트:** `ai-agent-study-group/job-matching-agent`
- **관련 이슈:** [#48 — Cloud provider Railway](https://github.com/ai-agent-study-group/job-matching-agent/issues/48)
- **작성일:** 2026-11-17
- **배포 대상:** Python 3.12 / FastAPI / FastMCP 백엔드
- **배포 방식:** GitHub 저장소 연결 → 루트 `Dockerfile` 빌드 → Railway Service 실행
- **확인된 공개 주소:** `https://job-matching-agent-production-7884928e.up.railway.app`

### 1. 목적과 배포 구조

외부 AI 클라이언트가 Job Matching Agent의 MCP 서버에 HTTPS로 접근할 수 있도록 Railway에 백엔드 서비스를 배포한다. 같은 FastAPI 프로세스에서 `/health`, `/mcp`, `/api`를 제공한다.

```text
GitHub: ai-agent-study-group/job-matching-agent
                    |
                    v
             Railway Project
                    |
              Backend Service
                    |
        Dockerfile (repository root)
                    |
     FastAPI + FastMCP (0.0.0.0:$PORT)
                    |
          Railway Public Domain
                    |
         +----------+----------+
         |                     |
      /health                 /mcp
    Health Check       MCP Client Connection
```

> **확인 범위:** 이슈와 댓글에서 Docker 배포, Shared Variables, 공개 도메인, `/health` 및 MCP 도구 조회 성공을 확인했다. 아래 클릭 순서는 동일한 환경을 재구성하기 위한 가이드이며, 실제 서비스 생성 당시의 모든 UI 동작을 기록한 것은 아니다.

### 2. Railway 프로젝트 및 서비스 생성

1. [Railway](https://railway.app/)에 로그인하여 **New Project**를 선택한다.
2. **Deploy from GitHub repo**를 선택하고 GitHub 연동을 승인한다.
3. `ai-agent-study-group/job-matching-agent` 저장소를 선택한다.
4. 프로젝트 내에 생성된 백엔드 **Service**의 **Settings / Source**에서 저장소와 배포 브랜치를 확인한다.
5. 빌드 설정에서 저장소 루트의 `Dockerfile`을 사용하도록 설정 또는 자동 감지 결과를 확인한다. 이 저장소의 Dockerfile은 루트 경로에 있다.
6. 필요한 변수를 설정한 뒤 최초 배포 또는 재배포를 진행한다. Railway **Deployments**와 빌드/런타임 로그에서 성공 여부를 확인한다.

**실제 Dockerfile 핵심 설정:**

```dockerfile
EXPOSE 8000
CMD ["sh", "-c", "uvicorn main:app --app-dir /app/src --host 0.0.0.0 --port ${PORT:-8000}"]
```

- Railway가 제공하는 `PORT`가 있으면 해당 포트로 실행하며, 없으면 `8000`을 사용한다.
- 외부 트래픽을 받도록 `0.0.0.0`에 바인딩한다.
- 별도 Start Command를 무조건 추가하지 않는다. 기존 Dockerfile의 `CMD`가 이미 실행 명령을 제공한다.
- 포트/라우팅에 문제가 생기면 Service **Settings → Networking**의 대상 포트와 실제 컨테이너 리스닝 포트를 비교한다.

### 3. Shared Variables 생성 및 서비스 연결

Shared Variables는 동일 Railway 환경 내에서 여러 서비스가 참조할 수 있는 공통 환경 변수다. **Shared Variable에 값을 만드는 것과 해당 Service에 참조를 연결하는 것은 별도 작업**이다.

1. Railway 프로젝트의 대상 환경(예: `production`)을 선택한다.
2. 프로젝트의 **Shared Variables** 영역에서 변수를 추가한다. Railway UI 버전에 따라 환경/프로젝트 변수 화면에서 접근한다.
3. 아래 변수 이름과 실제 값을 등록한다.
4. 백엔드 Service의 **Variables** 화면으로 이동해 각 Shared Variable을 서비스에 **참조 연결(Reference)** 한다. 단순히 공통 변수 저장소에 생성하는 것만으로 프로세스에서 읽을 수 있다고 가정하지 않는다.
5. 적용 예정 변경 사항을 배포(Deploy)하고, 새 런타임에 변수가 반영되었는지 앱 기동 로그로 확인한다. **비밀 값 자체는 로그에 남기지 않는다.**

| 변수 | 필수 여부 | 용도 | 값 예시 / 주의 |
|---|---|---|---|
| `LLM_MODEL` | 필수 | 서버 측 AI 모델 선택 | `openai:gpt-4.1-mini` (예시) |
| `OPENAI_API_KEY` | OpenAI 모델 선택 시 필수 | 서버 측 LLM 호출 인증 | 실제 값은 Railway에만 저장 |
| `ANTHROPIC_API_KEY` | Anthropic 모델 선택 시 필수 | 대체 모델 호출 인증 | 해당 모델을 선택한 경우에만 필요 |
| `LOGFIRE_TOKEN` | 선택 | Logfire 원격 관찰 | 관찰 기능을 사용할 때만 등록 |
| `PORT` | Railway 주입 | 웹 서버 리스닝 포트 | 직접 고정할 필요 없음 |

**Issue #48에서 실제 등록했다고 보고된 Shared Variables:** `LLM_MODEL`, `OPENAI_API_KEY`.

로컬 `.env` 예시(실제 API 키를 문서에 입력하지 말 것):

```dotenv
LLM_MODEL=openai:gpt-4.1-mini
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

- `.env` 파일이나 API 키를 Git에 커밋하지 않는다.
- Shared Variable 참조/서비스 바인딩이 잘못되면 `LLM_MODEL` 누락으로 앱이 시작되지 않을 수 있다.
- `production`과 기타 Railway 환경의 Shared Variables는 별도로 검토한다.
- 접근 권한은 최소화하고, 키 유출 의심 시 API 제공자에서 교체한다.

### 4. Public Domain 생성

1. Railway 프로젝트에서 배포된 백엔드 Service를 연다.
2. **Settings → Networking → Public Networking**으로 이동한다.
3. **Generate Domain**을 선택한다.
4. Railway가 생성한 `*.up.railway.app` 도메인을 확인하고, 필요한 경우 서비스가 수신하는 포트를 지정한다.
5. 도메인을 통해 HTTPS 요청이 정상 전달되는지 확인한다.

**Issue #48에서 확인된 Railway 제공 도메인:**

```text
https://job-matching-agent-production-7884928e.up.railway.app
```

이는 Railway가 제공하는 공개 도메인이다. **별도 소유 도메인을 DNS/CNAME으로 연결하는 'Custom Domain' 작업과 구별**해야 한다. 이슈 #48 자체에서도 별도 커스텀 도메인 연결은 범위 제외로 기재되어 있다.

### 5. 배포 검증

#### 5.1 Health Check

```bash
BASE_URL="https://job-matching-agent-production-7884928e.up.railway.app"
curl -i "$BASE_URL/health"
```

이슈에 기록된 응답 본문:

```json
{"status":"ok"}
```

- **검증 결과:** 성공. 공개 HTTPS 도메인에서 `/health` 응답을 받았다.
- Railway의 배포 로그에서도 앱 시작 오류, 환경 변수 누락 및 포트 바인딩 오류 여부를 확인한다.

#### 5.2 MCP endpoint

```text
https://job-matching-agent-production-7884928e.up.railway.app/mcp
```

`/mcp`는 단순 REST GET API가 아니라 **MCP Streamable HTTP** 프로토콜을 사용한다. 세션 초기화 없이 다음 명령만 실행하면:

```bash
curl "$BASE_URL/mcp"
```

기록된 결과는 다음과 같다.

```json
{"jsonrpc":"2.0","id":null,"error":{"code":-32600,"message":"Bad Request: Missing session ID"}}
```

이는 **초기화하지 않은 GET 요청에 대한 응답**이므로, 이것만으로 MCP 서비스가 고장 났다고 판단할 수 없다. 실제 클라이언트 동작은 `initialize` → `notifications/initialized` → `tools/list`로 확인한다.

```bash
# FastMCP 클라이언트가 설치된 환경에서 간편하게 확인
uv run fastmcp list "$BASE_URL/mcp"
```

또는 이슈 댓글처럼 Streamable HTTP 요청을 직접 보내 `initialize` 응답의 `Mcp-Session-Id`를 이후 요청 헤더에 전달한다. 세션 ID는 비밀값처럼 취급해 공개 로그에 기록하지 않는다.

**Issue #48의 실제 검증 기록:**

| 검증 항목 | 결과 |
|---|---|
| MCP `initialize` | `HTTP 200`, `text/event-stream`, 세션 ID 수신 |
| `notifications/initialized` | `HTTP 202 Accepted` |
| `tools/list` | 성공 |
| 확인된 서버 | `jobs` / version `4.1.3` (당시 응답) |
| 확인된 도구 | `list_sources`, `get_usage`, `search_jobs`, `get_job` |

상세 요청 및 실제 응답: [Issue #48 MCP 검증 댓글](https://github.com/ai-agent-study-group/job-matching-agent/issues/48#issuecomment-6950642409).

### 6. 트러블슈팅 및 운영 주의사항

| 증상 | 확인 사항 / 조치 |
|---|---|
| Docker 빌드 실패 | 루트 `Dockerfile`, `uv.lock`, 빌드 로그 확인 |
| App startup 실패 | `LLM_MODEL`과 모델에 대응하는 API 키가 서비스 변수로 연결되어 있는지 확인 |
| 502/503 또는 접속 불가 | Railway 실행 상태, `PORT`, `0.0.0.0` 바인딩, Public Networking 대상 포트 확인 |
| `/health` 실패 | 서비스 Deployments/Logs 및 FastAPI 부팅 오류 확인 |
| `/mcp`에서 `Missing session ID` | 단순 GET 대신 MCP 클라이언트로 초기화 후 도구 조회 |
| 변수 변경 후 반영되지 않음 | 환경 및 참조 연결 상태 확인 후 변경 사항을 배포 |

**보안 고려사항**

- `/mcp`는 외부에서 접근 가능한 공개 endpoint이다. 인증 및 호출 제한 정책은 별도 작업으로 다룬다.
- API 키를 레포지토리, 스크린샷, 이슈 댓글, 클라이언트 JavaScript에 노출하지 않는다.
- Health Check 성공만으로 API 기능·MCP 인증·장애 대응을 전부 검증했다고 간주하지 않는다.
- 운영 중 로그, 리소스 사용량, 과금과 비밀 값 접근 권한을 주기적으로 검토한다.

### 7. 완료 상태 (2026-11-17, Issue #48 기록 기준)

- [x] Railway 서비스 Docker 이미지 빌드 및 배포 성공
- [x] `LLM_MODEL`, `OPENAI_API_KEY` Shared Variables 등록 보고
- [x] Railway 제공 공개 HTTPS 도메인 생성
- [x] 공개 `/health` 응답 확인
- [x] MCP 초기화 및 `tools/list`에서 도구 4개 확인
- [x] 배포 설정과 검증 결과를 이슈 댓글에 기록
- [ ] 인증·호출 제한 등 운영 보안 강화는 별도 이슈에서 결정

### 8. 참고 자료 및 스크린샷

- [GitHub Issue #48](https://github.com/ai-agent-study-group/job-matching-agent/issues/48)
- [배포·Shared Variables·도메인 확인 댓글](https://github.com/ai-agent-study-group/job-matching-agent/issues/48#issuecomment-6946570472)
- [Shared Variables 스크린샷](https://github.com/user-attachments/assets/81ef1c47-c795-4889-a829-a26d7240c602)
- [Public Networking 스크린샷](https://github.com/user-attachments/assets/79649a94-8c93-499b-96dc-7a368ee8d079)
- [MCP Streamable HTTP 최종 검증 댓글](https://github.com/ai-agent-study-group/job-matching-agent/issues/48#issuecomment-6950642409)
- [저장소 Dockerfile](https://github.com/ai-agent-study-group/job-matching-agent/blob/main/Dockerfile)
- [Railway Services 문서](https://docs.railway.com/services)
- [Railway Variables 문서](https://docs.railway.com/variables)
- [Railway Public Networking 문서](https://docs.railway.com/networking/public-networking)
