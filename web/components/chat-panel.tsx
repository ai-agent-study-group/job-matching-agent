"use client";
import { useEffect, useRef, useState } from "react";
import {
  ArrowUp,
  BookOpen,
  ChevronDown,
  ExternalLink,
  RotateCcw,
  Search,
  Compass,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useChat } from "@/hooks/use-chat";
import { domains } from "@/lib/agents/domains";
import type { Domain } from "@/lib/types";
export function ChatPanel({ domain }: { domain: Domain }) {
  const config = domains[domain];
  const { messages, busy, error, send, reset } = useChat(domain);
  const [input, setInput] = useState("");
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (messages.length)
      end.current?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }, [messages, busy]);
  async function submit() {
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    await send(text);
  }
  return (
    <div className="soft-card flex min-h-[570px] flex-col overflow-hidden">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4 sm:px-7">
        <div className="flex items-center gap-3">
          <span className="flex size-9 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
            <Compass size={19} />
          </span>
          <div>
            <h2 className="text-sm font-semibold">{config.label}</h2>
            <p className="mt-1 text-xs text-slate-500">
              로컬 공고 · 규칙 기반 데모
            </p>
          </div>
        </div>
        <Button
          variant="ghost"
          onClick={() => {
            reset();
            setInput("");
          }}
          aria-label="대화 초기화"
          className="text-slate-500"
        >
          <RotateCcw size={14} />
          <span className="hidden sm:inline">초기화</span>
        </Button>
      </div>
      <div
        className="flex-1 space-y-6 px-5 py-7 sm:px-7"
        aria-live="polite"
        aria-busy={busy}
      >
        {!messages.length && (
          <div className="mx-auto max-w-md py-12 text-center">
            <span className="mx-auto flex size-14 items-center justify-center rounded-2xl bg-slate-50 text-slate-500">
              <BookOpen size={25} />
            </span>
            <h3 className="mt-5 text-lg font-semibold">
              궁금한 내용을 적어보세요
            </h3>
            <p className="mt-3 text-sm leading-7 text-slate-500">
              조건에 맞는 공고를 찾고 읽는 과정을 보여드립니다.
              <br />
              아래 예시 질문부터 시작해도 좋아요.
            </p>
            <div className="mt-6 flex flex-col gap-2">
              {config.examples.map((q) => (
                <button
                  key={q}
                  onClick={() => void send(q)}
                  className="rounded-xl border border-slate-200 px-4 py-3 text-left text-sm text-slate-600 transition hover:border-blue-300 hover:bg-blue-50"
                >
                  {q} <span className="float-right text-slate-500">↗</span>
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((message) => (
          <article
            key={message.id}
            className={
              message.role === "user"
                ? "ml-auto max-w-[88%] rounded-2xl rounded-tr-sm bg-blue-600 px-5 py-4 text-sm leading-7 text-white"
                : "max-w-[95%]"
            }
          >
            {message.role === "assistant" && (
              <p className="mb-2 text-xs font-medium text-slate-500">
                {config.label} · 데모
              </p>
            )}
            <p className="whitespace-pre-wrap break-words text-sm leading-7">
              {message.content}
            </p>
            {message.result && (
              <>
                <div className="mt-4 space-y-2">
                  {message.result.citations.map((source) => (
                    <a
                      key={source.id}
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-start justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-700"
                    >
                      <div>
                        <p className="text-xs font-medium">{source.title}</p>
                        <p className="mt-1 text-[11px] text-slate-500">
                          확인 {source.reviewedAt.slice(0, 10)} ·{" "}
                          {source.kind === "editorial_summary"
                            ? "채용공고의 학습용 요약"
                            : "검토된 수집 공고"}
                        </p>
                      </div>
                      <ExternalLink size={13} className="mt-1 shrink-0" />
                    </a>
                  ))}
                </div>
                <details className="mt-4 rounded-xl border border-dashed border-slate-200 p-3">
                  <summary className="flex cursor-pointer items-center gap-2 text-xs text-slate-500">
                    <Search size={13} />
                    활동 기록 {message.result.activities.length}개
                    <ChevronDown size={13} />
                  </summary>
                  <ol className="mt-4 space-y-3">
                    {message.result.activities.map((activity, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="flex size-5 shrink-0 items-center justify-center rounded-full bg-slate-100 text-[10px] text-slate-500">
                          {i + 1}
                        </span>
                        <div>
                          <p className="text-xs font-medium text-slate-700">
                            {activity.label}
                          </p>
                          <p className="mt-1 break-words text-xs leading-5 text-slate-500">
                            {activity.detail}
                          </p>
                        </div>
                      </li>
                    ))}
                  </ol>
                </details>
              </>
            )}
          </article>
        ))}
        {busy && (
          <p className="animate-pulse text-sm text-slate-500" role="status">
            데모 실행 중…
          </p>
        )}
        <div ref={end} />
      </div>
      <div className="border-t border-slate-100 p-5 sm:p-6">
        {error && (
          <p role="alert" className="mb-3 text-sm text-red-600">
            {error}
          </p>
        )}
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void submit();
          }}
        >
          <label htmlFor="question" className="sr-only">
            질문 입력
          </label>
          <div className="relative">
            <Textarea
              id="question"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              maxLength={2000}
              disabled={busy}
              placeholder="궁금한 내용을 한국어로 입력하세요"
              className="min-h-24 resize-none rounded-2xl bg-slate-50 p-4 pr-16"
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey &&
                  !event.nativeEvent.isComposing
                ) {
                  event.preventDefault();
                  void submit();
                }
              }}
            />
            <Button
              type="submit"
              size="icon"
              disabled={busy || !input.trim()}
              aria-label="질문 보내기"
              className="absolute right-3 bottom-3 rounded-xl"
            >
              <ArrowUp size={18} />
            </Button>
          </div>
          <p className="mt-3 text-center text-[11px] text-slate-500">
            Enter 전송 · Shift+Enter 줄바꿈 · 새로고침하면 대화가 초기화됩니다.
          </p>
        </form>
      </div>
    </div>
  );
}
