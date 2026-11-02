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

  async function send(text: string) {
    if (busy || !text.trim()) return;
    const prev = messages;
    const next: Message[] = [
      ...prev,
      { id: crypto.randomUUID(), role: "user", content: text.trim() },
    ];
    setMessages(next);
    setBusy(true);
    setError("");
    try {
      const turns: Turn[] = next
        .slice(-11)
        .map(({ role, content }) => ({ role, content }));
      const result = await runAgent(domain, turns);
      setMessages([
        ...next,
        { id: crypto.randomUUID(), role: "assistant", content: result.answer, result },
      ]);
    } catch {
      setMessages(prev);
      setError("응답을 준비하지 못했습니다. 다시 시도해주세요.");
    } finally {
      setBusy(false);
    }
  }

  return { messages, busy, error, send, reset };
}
