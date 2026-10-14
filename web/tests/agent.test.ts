import test from "node:test";
import assert from "node:assert/strict";
import { runAgent } from "../lib/agents/run";
import { searchSources, readSource } from "../lib/tools/sources";
import { validSource } from "../lib/sources/repository";
import { POST } from "../app/api/chat/route";
import type { ModelProvider } from "../lib/providers/types";
import type { Source } from "../lib/types";

test("백엔드: 실제 검색→읽기→출처", async () => {
  const result = await runAgent("backend", [
    { role: "user", content: "Java Spring 백엔드" },
  ]);
  assert.deepEqual(
    result.activities.map((a) => a.type),
    ["search", "read", "answer"],
  );
  assert.equal(result.citations[0].id, "backend-fintech");
  assert.match(result.answer, /Spring/);
});
test("분야별 공고와 읽기 격리", async () => {
  assert.equal((await searchSources("backend", "RAG LLM 파이프라인")).length, 0);
  assert.equal(await readSource("backend", "data-ml"), null);
  assert.equal(await readSource("data", "backend-fintech"), null);
});
test("근거 없음", async () => {
  const result = await runAgent("backend", [
    { role: "user", content: "xyzxyz" },
  ]);
  assert.equal(result.citations.length, 0);
  assert.match(result.answer, /아직 없습니다/);
  assert.deepEqual(
    result.activities.map((a) => a.type),
    ["search", "answer"],
  );
});
test("공고가 있어도 연봉 정보는 보류", async () => {
  const result = await runAgent("backend", [
    { role: "user", content: "Java 백엔드 공고의 연봉은 얼마인가요?" },
  ]);
  assert.match(result.answer, /연봉/);
  assert.equal(result.citations[0].id, "backend-fintech");
});
test("모호한 추천 요청 되묻기 후 맥락 유지", async () => {
  const first = await runAgent("data", [
    { role: "user", content: "공고 추천해주세요" },
  ]);
  assert.match(first.answer, /어떤 직무/);
  assert.equal(first.citations.length, 0);
  const second = await runAgent("data", [
    { role: "user", content: "공고 추천해주세요" },
    { role: "assistant", content: first.answer },
    { role: "user", content: "Python RAG 경험 있어요" },
  ]);
  assert.equal(second.citations[0].id, "data-ml");
  assert.match(second.answer, /직무·기술 기준/);
});
test("반복 도구 요청의 실행 한도", async () => {
  const provider: ModelProvider = {
    mode: "demo",
    async decide() {
      return {
        type: "tool_call",
        callId: "repeat",
        name: "search_sources",
        arguments: { query: "java" },
      };
    },
  };
  const result = await runAgent(
    "backend",
    [{ role: "user", content: "java" }],
    { provider },
  );
  assert.equal(result.activities.filter((a) => a.type === "search").length, 3);
  assert.equal(result.activities.at(-1)?.type, "limit");
});
test("미등록 도구와 잘못된 입력은 실행하지 않음", async () => {
  for (const [name, args] of [
    ["delete_file", { path: "x" }],
    ["search_sources", { query: 3 }],
    ["read_source", { id: "data-ml" }],
  ] as const) {
    const provider: ModelProvider = {
      mode: "demo",
      async decide({ toolResults }) {
        return toolResults.length
          ? { type: "answer", text: "error handled", sourceIds: [] }
          : { type: "tool_call", callId: "bad", name, arguments: args };
      },
    };
    const result = await runAgent(
      "backend",
      [{ role: "user", content: "java" }],
      { provider },
    );
    assert.equal(result.activities[0].type, "error");
  }
});
test("읽지 않은 공고의 인용과 중복 출처 제거", async () => {
  const provider: ModelProvider = {
    mode: "demo",
    async decide() {
      return {
        type: "answer",
        text: "answer",
        sourceIds: ["backend-fintech", "data-ml"],
      };
    },
  };
  const result = await runAgent("backend", [{ role: "user", content: "hi" }], {
    provider,
  });
  assert.deepEqual(result.citations, []);
});
test("저장소와 제공자 실패가 사용자 답변으로 처리됨", async () => {
  const result = await runAgent(
    "backend",
    [{ role: "user", content: "java" }],
    {
      repository: {
        async list() {
          throw new Error("unavailable");
        },
      },
    },
  );
  assert.equal(result.activities[0].type, "error");
  assert.equal(result.citations.length, 0);
  const provider: ModelProvider = {
    mode: "demo",
    async decide() {
      throw new Error("timeout");
    },
  };
  const failure = await runAgent("backend", [{ role: "user", content: "hi" }], {
    provider,
  });
  assert.match(failure.answer, /다시 시도/);
});
test("검토 대기와 잘못된 메타데이터는 제외", async () => {
  const source = await readSource("backend", "backend-fintech");
  assert.ok(source);
  assert.equal(validSource({ ...source, reviewed: false }, "backend"), false);
  assert.equal(
    validSource({ ...source, url: "javascript:bad" }, "backend"),
    false,
  );
  assert.equal(validSource({ ...source, domain: "data" }, "backend"), false);
  const results = await searchSources("backend", "java", {
    async list() {
      return [{ ...source, reviewed: false }] as Source[];
    },
  });
  assert.equal(results.length, 0);
});
test("API 입력 검증과 정상 실행", async () => {
  const call = (body: unknown) =>
    POST(
      new Request("http://localhost/api/chat", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    );
  assert.equal((await call({ domain: "other", messages: [] })).status, 400);
  assert.equal(
    (
      await call({
        domain: "backend",
        messages: [{ role: "assistant", content: "x" }],
      })
    ).status,
    400,
  );
  assert.equal(
    (
      await call({
        domain: "backend",
        messages: [{ role: "user", content: "x".repeat(2001) }],
      })
    ).status,
    400,
  );
  assert.equal((await call(null)).status, 400);
  const ok = await call({
    domain: "backend",
    messages: [{ role: "user", content: "java" }],
  });
  assert.equal(ok.status, 200);
  assert.equal((await ok.json()).mode, "demo");
});
