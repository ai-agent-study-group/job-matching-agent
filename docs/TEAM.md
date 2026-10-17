---
제목: "프로젝트 역할"
유형: "역할 안내"
설명: "채용 매칭 프로젝트의 역할과 직군별 작업 문서를 안내합니다."
관련문서: []
---

# 프로젝트 역할

아래 BE1·BE2·LLM1·LLM2·FE·DevOps·PO는 기존 역할 표기입니다. 기존 역할은 7개이고 팀은 6명이므로, 현재 필요한 작업에 맞춰 역할 구분을 다시 정한 뒤 담당자를 배정합니다. 아래 표는 개인 배정표가 아닙니다.

정기 모임은 기본적으로 **매주 화요일 18:00, Discord**에서 진행합니다. 역할 분담의 선택지는 [10월 20일 회의 안건](meetings/2026-10-20.md#4-역할-분담)에서 논의합니다.

| 구분 · 전체 이름 | 하는 일 | 기존 역할 표기 | 작업 문서 |
| --- | --- | --- | --- |
| 기획 / 제품 책임자(Product Owner, PO) | 매칭 기준, 사용자 흐름, 정답 라벨과 우선순위 | PO | [기획 폴더](po/README.md) |
| 프론트엔드(Front End, FE) | 공고 목록, 매칭 근거 대시보드, 이력 편집 화면 | FE | [프론트엔드 폴더](fe/README.md) |
| 백엔드(Back End, BE) | API, 저장·조회, 실행 연결과 공고 소스 어댑터 | BE1 · BE2 | [백엔드 폴더](be/README.md) |
| 인공지능·언어 모델(Artificial Intelligence / Large Language Model) | agent 구현·포트, 도구 연결, 요건별 매칭과 평가 | LLM1 · LLM2 | [인공지능·언어 모델 폴더](ai-llm/README.md) |
| 데이터 수집 | 사이트·API 조사, 검색·추출, 공고 소스 어댑터와 중복 처리 | BE1 · BE2 | [데이터 수집 폴더](data/README.md) |
| 인프라·개발 운영(Infrastructure / Development and Operations) | 배포, CI, 개발 환경과 운영 | DevOps | [인프라·개발 운영 폴더](infra/README.md) |

MCP 서버는 새로 생긴 작업으로 기존 담당 표기에 대응하지 않습니다. 공고 검색도 agent가 도구로 수행하는 구조를 검토합니다. Gmail 알림 수집은 PoC에서 제외하며, JD 사전 구조화는 추후 검토합니다. 스키마는 전원 합의 대상입니다.

직군별 폴더에 메모·작업 내용·결정·참고 자료를 작성합니다. Markdown 문서와 문서용 이미지만 바꾸면 PR은 선택 사항입니다.
코드·사이트 화면·설정을 함께 바꾸면 [기여 규칙](https://github.com/ai-agent-study-group/job-matching-agent/blob/main/CONTRIBUTING.md)을 따릅니다.

모듈별 작업 범위와 담당 상태는 [구조 안내](STRUCTURE.md)에서 확인합니다.
