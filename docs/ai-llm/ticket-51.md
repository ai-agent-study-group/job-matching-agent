
# Ticket #51 — Job Summarizer Agent

## 목표
MCP get_job으로 채용공고 상세 내용을 조회하고,
LLM Agent를 이용해 구조화된 JD로 변환한다.

## 구현 내용
- JD Pydantic 도메인 모델 추가
- Job Summarizer Agent 구현
- MCP get_job과 POST /api/jd 연결
- 필수/우대 기술 및 소프트 스킬 분리
- 필수/우대 언어 분리
- 담당 업무와 채용 요건 분리
- 명시되지 않은 조건은 추측하지 않음
- 공고 메타데이터는 원본 유지

## 처리 흐름
POST /api/jd
→ MCP get_job(source, posting_id)
→ JobPosting
→ Job Summarizer Agent
→ JD

## 설계 결정
- Agent 생성은 job_summarizer.py에서 담당
- Agent 실행과 MCP 호출은 route.py에서 담당
- output_type=JD로 출력 구조 검증
- 기존 POST /api/search 동작 유지
- 공고 한 건씩 분석하며 일괄 분석은 제외

## 테스트
- TestModel을 이용한 JD 구조 검증
- FakeSource를 이용한 MCP/API 통합 테스트
- 공고 본문 누락 및 조회 실패 테스트
- 실제 Arbeitsagentur 공고로 수동 검증
- Ruff 및 전체 pytest 실행

## 범위 제외
- 매칭 점수 계산
- Matching Agent
- DB 저장
- 대량 공고 자동 분석
