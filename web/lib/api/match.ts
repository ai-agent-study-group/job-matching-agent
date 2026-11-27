import type { components } from "@/lib/api-types/api.generated";

type JobPosting = components["schemas"]["JobPosting"];

// ponytail: #81 도메인 초안을 손으로 옮긴 타입. #81 merge 뒤 api.generated의 MatchResult로 바꿈
export type Check = {
  target: string;
  kind:
    | "requirement"
    | "nice_to_have"
    | "responsibility"
    | "skill"
    | "qualification"
    | "condition";
  verdict: "met" | "partial" | "unmet" | "unknown";
  evidence: string | null;
};

export type MatchResult = {
  source: string;
  posting_id: string;
  checks: Check[];
  /** 0~1. BE가 checks로 계산 */
  score: number;
};

/** 결과 화면 한 줄: 공고 요약 + 매칭 결과 */
export type Match = {
  posting: Pick<JobPosting, "source" | "id" | "company" | "title" | "location">;
  result: MatchResult;
};

const MOCK: Match[] = [
  {
    posting: {
      source: "arbeitsagentur",
      id: "10001-1000000001-S",
      company: "Acme Payments GmbH",
      title: "Senior Backend Engineer (Java)",
      location: "Berlin",
    },
    result: {
      source: "arbeitsagentur",
      posting_id: "10001-1000000001-S",
      score: 0.82,
      checks: [
        {
          target: "Mehrjährige Erfahrung mit Java und Spring Boot",
          kind: "requirement",
          verdict: "met",
          evidence:
            "Spring Boot 기반 결제 API를 설계·운영하며 일 200만 건 트래픽 처리",
        },
        {
          target: "Erfahrung mit relationalen Datenbanken",
          kind: "requirement",
          verdict: "met",
          evidence: "MySQL 쿼리 튜닝으로 정산 배치 시간을 40% 단축",
        },
        {
          target: "Kenntnisse in Kubernetes und AWS",
          kind: "nice_to_have",
          verdict: "partial",
          evidence:
            "Docker로 서비스 컨테이너화, 사내 Kubernetes 클러스터에 배포",
        },
        {
          target: "Erfahrung im Zahlungsverkehr",
          kind: "nice_to_have",
          verdict: "met",
          evidence: "PG사 연동과 정산 시스템 개발",
        },
        { target: "Java", kind: "skill", verdict: "met", evidence: null },
        { target: "Kafka", kind: "skill", verdict: "unmet", evidence: null },
        {
          target: "min_years: 4",
          kind: "qualification",
          verdict: "met",
          evidence: null,
        },
        {
          target: "work_modes: hybrid",
          kind: "condition",
          verdict: "unknown",
          evidence: null,
        },
      ],
    },
  },
  {
    posting: {
      source: "arbeitsagentur",
      id: "10001-1000000002-S",
      company: "Datenwerk AG",
      title: "Data Engineer (m/w/d)",
      location: "München",
    },
    result: {
      source: "arbeitsagentur",
      posting_id: "10001-1000000002-S",
      score: 0.54,
      checks: [
        {
          target: "Aufbau und Betrieb von Datenpipelines",
          kind: "requirement",
          verdict: "partial",
          evidence: "MySQL 쿼리 튜닝으로 정산 배치 시간을 40% 단축",
        },
        {
          target: "Sehr gute Python-Kenntnisse",
          kind: "requirement",
          verdict: "unmet",
          evidence: null,
        },
        {
          target: "Verantwortung für das Data Warehouse",
          kind: "responsibility",
          verdict: "unknown",
          evidence: null,
        },
        { target: "SQL", kind: "skill", verdict: "met", evidence: null },
        {
          target: "language: de (fluent)",
          kind: "qualification",
          verdict: "partial",
          evidence: null,
        },
      ],
    },
  },
  {
    posting: {
      source: "arbeitsagentur",
      id: "10001-1000000003-S",
      company: "Nordlicht Software",
      title: "Frontend Developer React",
      location: "Hamburg",
    },
    result: {
      source: "arbeitsagentur",
      posting_id: "10001-1000000003-S",
      score: 0.21,
      checks: [
        {
          target: "Mehrjährige Erfahrung mit React und TypeScript",
          kind: "requirement",
          verdict: "unmet",
          evidence: null,
        },
        {
          target: "REST-APIs anbinden",
          kind: "requirement",
          verdict: "met",
          evidence:
            "Spring Boot 기반 결제 API를 설계·운영하며 일 200만 건 트래픽 처리",
        },
        { target: "React", kind: "skill", verdict: "unmet", evidence: null },
      ],
    },
  },
];

/** 목 데이터를 쓰는 동안 true. 화면이 MockAlert를 띄움. fetch로 바꿀 때 지움 */
export const IS_MOCK = true;

// ponytail: 목 데이터. #70 매칭 API merge 뒤 fetch로 바꿈 (호출부는 그대로)
export const getMatches = async (): Promise<Match[]> =>
  [...MOCK].sort((a, b) => b.result.score - a.result.score);

export const getMatch = async (source: string, id: string) =>
  MOCK.find((m) => m.posting.source === source && m.posting.id === id) ?? null;
