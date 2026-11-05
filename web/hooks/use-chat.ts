"use client";
import { useState } from "react";
import type { ChatResult, Domain, Turn } from "@/domain/matching/types";
import { runAgent } from "@/domain/matching/agent";

export interface Message extends Turn {
  id: string;
  result?: ChatResult;
}

// 목 에이전트를 직접 호출한다. 백엔드가 붙으면 runAgent 자리를 fetch("/api/chat")로 교체하고
// AbortController·타임아웃을 다시 넣는다(목은 로컬·즉시 응답이라 불필요).
export function useChat(domain: Domain) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  function reset() {
    setMessages([]);
    setError("");
    setBusy(false);
  }

  // 사용자 말풍선이 이미 messages에 있는 상태에서 응답만 생성한다. send는 턴을 추가한 뒤,
  // retry는 추가 없이(실패한 마지막 사용자 턴 유지) 호출한다.
  async function run(history: Message[]) {
    setBusy(true);
    setError("");
    try {
      const turns: Turn[] = history
        .slice(-11)
        .map(({ role, content }) => ({ role, content }));
      const result = await runAgent(domain, turns);
      setMessages([
        ...history,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: result.answer,
          result,
        },
      ]);
    } catch {
      // 사용자 말풍선은 유지하고 에러만 노출 — 입력창은 이미 비워져 재입력 부담이 큼.
      setError("응답을 준비하지 못했습니다. 다시 시도해주세요.");
    } finally {
      setBusy(false);
    }
  }

  async function send(text: string) {
    if (busy || !text.trim()) return;
    const next: Message[] = [
      ...messages,
      { id: crypto.randomUUID(), role: "user", content: text.trim() },
    ];
    setMessages(next);
    await run(next);
  }

  function retry() {
    if (busy || messages.at(-1)?.role !== "user") return;
    void run(messages);
  }

  return { messages, busy, error, send, retry, reset };
}
