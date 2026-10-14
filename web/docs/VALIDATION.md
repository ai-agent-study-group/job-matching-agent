# 검증 기록

germany-life-agent 구조를 기반으로 이력서 매칭 도메인에 맞춰 코드·문서를 교체한 초기 스캐폴드입니다.

## 실행해야 할 검증

```bash
npm install
npm run lint
npm run typecheck
npm test
npm run build
npm run test:scrape   # Python 의존성 설치 후
```

## 현재 상태

- 두 직무 분야(backend·data) 공고 요약과 규칙 기반 매칭 데모를 포함합니다.
- 에이전트/API 자동 테스트와 Python 수집 테스트를 도메인에 맞게 재작성했습니다.
- 실제 AI 호출은 구현하지 않았으므로 모델의 매칭 품질과 도구 선택 능력은 검증하지 않았습니다.
- 매칭 점수 계산, 알림, 자소서 초안은 미구현(확장 과제)입니다.

## 수집 관련

- 기본 앱 공고는 사람이 작성한 예시 요약입니다. 실제 채용 데이터가 아닙니다.
- 채용 사이트 수집은 robots.txt·이용약관 확인과 공식 API 사용을 전제로 합니다. 차단을 우회하지 않습니다.
- `weworkremotely.com` 수집 성공 여부는 사이트 HTML 구조에 따라 달라질 수 있으며, selector 수정이 필요할 수 있습니다.

실제 배포 전 관리자 인증, 개인정보(이력서) 처리 정책, 매칭 정확도 검증이 필요합니다.
