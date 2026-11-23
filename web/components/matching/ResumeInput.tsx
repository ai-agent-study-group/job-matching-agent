"use client";

import { useState } from "react";

type ResumeInputProps = {
  onContinue: () => void;
};

export const ResumeInput = ({ onContinue }: ResumeInputProps) => {
  const [mode, setMode] = useState<"file" | "text">("file");
  const [file, setFile] = useState<File | null>(null);
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  const handleContinue = () => {
    if (mode === "file" && (!file || !/\.(pdf|docx)$/i.test(file.name))) {
      setError("PDF 또는 DOCX 파일을 선택해 주세요.");
      return;
    }

    if (mode === "text" && !text.trim()) {
      setError("이력서 내용을 입력해 주세요.");
      return;
    }

    setError("");
    onContinue();
  };

  return (
    <section className="rounded-xl border p-6">
      <h2 className="text-lg font-semibold">이력서 입력</h2>

      <div className="my-4 flex gap-2" role="group" aria-label="입력 방식">
        <button
          type="button"
          className="rounded-md border px-3 py-2 aria-pressed:bg-muted"
          aria-pressed={mode === "file"}
          onClick={() => {
            setMode("file");
            setError("");
          }}
        >
          파일 선택
        </button>

        <button
          type="button"
          className="rounded-md border px-3 py-2 aria-pressed:bg-muted"
          aria-pressed={mode === "text"}
          onClick={() => {
            setMode("text");
            setError("");
          }}
        >
          텍스트 입력
        </button>
      </div>

      <div hidden={mode !== "file"}>
        <label htmlFor="resume-file" className="mb-2 block">
          PDF 또는 DOCX 이력서
        </label>
        <input
          id="resume-file"
          type="file"
          accept=".pdf,.docx"
          onChange={(event) => {
            setFile(event.currentTarget.files?.[0] ?? null);
            setError("");
          }}
        />
        {file && <p className="mt-2 break-all text-sm">{file.name}</p>}
      </div>

      <div hidden={mode !== "text"}>
        <label htmlFor="resume-text" className="mb-2 block">
          이력서 내용
        </label>
        <textarea
          id="resume-text"
          rows={5}
          className="w-full rounded-md border p-3"
          value={text}
          onChange={(event) => {
            setText(event.currentTarget.value);
            setError("");
          }}
        />
      </div>

      {error && (
        <p role="alert" className="mt-3 text-sm text-destructive">
          {error}
        </p>
      )}

      <button
        type="button"
        className="mt-4 rounded-md border px-4 py-2"
        onClick={handleContinue}
      >
        예시 추출 결과 보기
      </button>
    </section>
  );
};