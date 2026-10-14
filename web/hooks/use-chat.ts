"use client";
import { useEffect, useRef, useState } from "react";
import type { ChatResult, Domain, Turn } from "@/lib/types";
export interface Message extends Turn {
  id: string;
  result?: ChatResult;
}
export function useChat(domain: Domain) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const controller = useRef<AbortController | null>(null);
  const version = useRef(0);
  useEffect(
    () => () => {
      version.current++;
      controller.current?.abort();
    },
    [],
  );
  function reset() {
    version.current++;
    controller.current?.abort();
    controller.current = null;
    setMessages([]);
    setError("");
    setBusy(false);
  }
  async function send(text: string) {
    if (busy || !text.trim()) return;
    const revision = ++version.current;
    const abort = new AbortController();
    controller.current = abort;
    const next = [
      ...messages,
      { id: crypto.randomUUID(), role: "user" as const, content: text.trim() },
    ];
    setMessages(next);
    setBusy(true);
    setError("");
    const timeout = setTimeout(() => abort.abort(), 20000);
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: abort.signal,
        body: JSON.stringify({
          domain,
          messages: next
            .slice(-11)
            .map(({ role, content }) => ({ role, content })),
        }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error ?? "요청에 실패했습니다.");
      if (revision !== version.current) return;
      setMessages([
        ...next,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: result.answer,
          result,
        },
      ]);
    } catch (e) {
      if (revision === version.current) {
        setMessages(messages);
        setError(
          e instanceof Error && e.name !== "AbortError"
            ? e.message
            : "응답 시간이 초과되었습니다. 다시 시도해주세요.",
        );
      }
    } finally {
      clearTimeout(timeout);
      if (revision === version.current) {
        setBusy(false);
        controller.current = null;
      }
    }
  }
  return { messages, busy, error, send, reset };
}
