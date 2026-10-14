# 공고 수집과 검토

## 기본 예제

사람이 작성한 짧은 한국어 공고 요약 4건입니다. `kind: editorial_summary`로 수집 원문과 구분합니다.
실제 채용 공고가 아니라 매칭 흐름을 설명하기 위한 예시이며, 연봉·전형 일정은 포함하지 않습니다.

| 분야      | 공고 요약                      | 핵심 기술                       |
| --------- | ------------------------------ | ------------------------------- |
| 백엔드    | 핀테크 — 백엔드 엔지니어       | Java·Spring·Kubernetes·AWS·MSA  |
| 백엔드    | 커머스 — 서버 개발자           | Node·TypeScript·트래픽·Redis    |
| 데이터·AI | AI 플랫폼 — ML 엔지니어        | Python·PyTorch·LLM·RAG·MLOps    |
| 데이터·AI | 데이터 조직 — 데이터 엔지니어  | SQL·Spark·Airflow·ETL           |

개별 합격 가능성, 연봉, 회사별 전형 절차를 판단할 자료는 없습니다.

## 추가하는 순서

1. 수집할 채용 사이트와 조건 범위를 정합니다. sources.json에 ID·분야·URL·본문 selector·기술 키워드를 추가합니다.
2. 수집합니다. collect.py는 https 허용 호스트만 허용하고 자동으로 다른 링크를 따라 수집하지 않습니다.
3. pending 파일에서 본문 누락, 중복, 광고, 게시일과 수집일 차이를 확인합니다.
4. 원문과 비교하고 필요하면 짧은 한국어 요약을 작성합니다. 편집 언어도 갱신합니다.
5. review.py --approve <id>를 실행합니다. reviewedAt은 승인일입니다.
6. 앱에서 매칭을 실행하고 출처가 내용을 뒷받침하는지 확인합니다.

채용 플랫폼은 HTML 구조가 자주 바뀌고 수집을 차단할 수 있습니다. robots.txt와 이용약관을 확인하고 공식 API를 우선합니다.
수집은 20초 요청 제한, 2MB 응답 제한, 페이지 사이 0.3초 간격을 둡니다.
자동 승인과 정기 갱신은 없습니다. pending에는 저작권이 있는 공고 본문이 포함될 수 있어 기본 Git 제외합니다.

JSON 공통 필드: id, domain, title, body, url, keywords, collectedAt, reviewedAt, reviewed, language, kind.

## 수집 호스트와 차단

허용 호스트(`ALLOWED_HOSTS`)는 현재 `weworkremotely.com`과 `www.linkedin.com`입니다.
We Work Remotely는 공개 공고 목록이라 수집 실습 대상으로 사용합니다. 구조 변경 시 selector를 고쳐야 합니다.
링크드인 등 대부분의 플랫폼은 자동 수집을 차단하거나 약관으로 금지하며 공식 API를 요구합니다. 우회하지 않습니다.
차단 동작을 관찰하려면 `python3 scripts/scrape/collect.py --manifest scripts/scrape/linkedin-example.json`을 실행하세요.

## 한 페이지로 실습하기

```bash
# 백엔드 공고 목록 한 건만 검토 대기 파일로 수집
python3 scripts/scrape/collect.py --manifest scripts/scrape/backend-example.json

# 원문과 data/pending/wwr-backend.json을 직접 비교한 뒤에만 실행
python3 scripts/scrape/review.py --approve wwr-backend
```

수집만 하면 앱 공고는 바뀌지 않습니다. 승인하면 같은 ID의 기존 앱 공고가 교체됩니다.
현재 `section.jobs li` 본문을 선택하고 메뉴·스타일·스크립트는 제외합니다. 페이지 제목과 키워드는 수집 목록에서 지정합니다.

### 저장되는 JSON 구조

아래 body와 시각은 설명용 자리표시자입니다. 실제 파일은 공고 본문과 실제 수집 시각을 포함합니다.

```json
{
  "id": "wwr-backend",
  "domain": "backend",
  "title": "원격 백엔드 공고 목록 — We Work Remotely",
  "url": "https://weworkremotely.com/categories/remote-back-end-programming-jobs",
  "keywords": ["java", "spring", "백엔드"],
  "language": "en",
  "body": "여기에 추출한 공고 목록 본문이 저장됩니다.",
  "collectedAt": "<실제 수집 시각: UTC>",
  "reviewed": false,
  "reviewedAt": "",
  "kind": "scraped"
}
```

원문과 본문을 비교하고 검색 키워드를 보완한 뒤 승인합니다. 검토 대기 파일은 매칭에서 읽지 않습니다.
기본 예시 공고(사람 작성 요약)와 수집할 사이트 목록은 서로 다른 자료입니다.
