/** 이력서 입력 칸의 기본값. 프로필 화면의 모든 칸(재직 중 · 연도만 있는 날짜 포함)이 채워지는 예시 */
export const SAMPLE_RESUME = `Senior Backend Engineer
Acme Payments GmbH, Berlin | 2021-04 – heute
- Spring Boot 기반 결제 API를 설계·운영하며 일 200만 건 트래픽 처리
- Kafka로 정산 이벤트 파이프라인 구축, 정산 지연 40% 단축
- Kubernetes(AWS EKS) 배포 자동화

Backend Developer
Nordlicht Software, Hamburg | 2018 – 2021
- Java·MySQL로 사내 주문 관리 시스템 개발
- REST API 설계 및 테스트 자동화(JUnit)

학력
M.Sc. Informatik, TU Berlin, 2018

기술
Java, Spring Boot, Kafka, MySQL, Docker, Kubernetes, AWS

언어
한국어(모국어), 독일어(유창), 영어(능숙)`;

/** 이력서 글 길이 범위(앞뒤 공백 뺀 글자 수). 짧으면 LLM이 뽑을 게 없고, 길면 비용 · 시간만 늚. A4 10장 ≈ 2만 자 */
export const RESUME_MIN_LENGTH = 50;
export const RESUME_MAX_LENGTH = 20_000;
