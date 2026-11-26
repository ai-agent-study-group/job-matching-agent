"use client";

import { useEffect, useState } from "react";
import { JobList } from "./JobList";
import { MatchingSteps } from "./MatchingSteps";
import { ProfileSummary } from "./ProfileSummary";
import { ResumeInput } from "./ResumeInput";

export const MatchingFlow = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [searchStatus, setSearchStatus] = useState<
    "idle" | "loading" | "error"
  >("idle");

  const [showEmpty, setShowEmpty] = useState(false);

  const startSearch = (empty: boolean) => {
    setShowEmpty(empty);
    setSearchStatus("loading");
  };

  useEffect(() => {
    if (currentStep !== 3 || searchStatus !== "loading") return;

    const timer = window.setTimeout(() => {
      setSearchStatus("idle");
      setCurrentStep(4);
    }, 800);

    return () => window.clearTimeout(timer);
  }, [currentStep, searchStatus]);

  return +(
    <section aria-label="이력서 매칭 데모" className="space-y-6 py-8">
      <MatchingSteps currentStep={currentStep} />

      <div hidden={currentStep !== 1}>
        <ResumeInput onContinue={() => setCurrentStep(2)} />
      </div>

      {currentStep === 2 && (
        <ProfileSummary
          jobTitles={["백엔드 개발자", "서버 개발자"]}
          locations={["서울", "부산"]}
        />
      )}

      {currentStep === 3 && (
        <section className="space-y-4 rounded-xl border p-6">
          <h2 className="text-lg font-semibold">공고 검색 · 예시</h2>

          {searchStatus === "loading" && (
            <p role="status">공고를 검색 중이에요…</p>
          )}

          {searchStatus === "error" && (
            <p role="alert" className="text-destructive">
              예시 오류. 공고를 불러오지 못했어요. 다시 시도해 주세요.
            </p>
          )}

          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className="rounded-md border px-4 py-2 disabled:opacity-50"
              disabled={searchStatus === "loading"}
              onClick={() => startSearch(false)}
            >
              {searchStatus === "error" ? "다시 시도" : "예시 검색 시작"}
            </button>
            <button
              type="button"
              className="rounded-md border px-4 py-2 disabled:opacity-50"
              disabled={searchStatus === "loading"}
              onClick={() => setSearchStatus("error")}
            >
              오류 예시 보기
            </button>
            <button
              type="button"
              className="rounded-md border px-4 py-2 disabled:opacity-50"
              disabled={searchStatus === "loading"}
              onClick={() => startSearch(true)}
            >
              빈 결과 예시 보기
            </button>
          </div>
        </section>
      )}

      {currentStep === 4 && <JobList showEmpty={showEmpty} />}

      <div className="flex gap-2">
        {currentStep > 1 && (
          <button
            type="button"
            className="rounded-md border px-4 py-2"
            onClick={() => {
              setSearchStatus("idle");
              setCurrentStep(currentStep - 1);
            }}
          >
            이전
          </button>
        )}

        {currentStep === 2 && (
          <button
            type="button"
            className="rounded-md border px-4 py-2"
            onClick={() => setCurrentStep(3)}
          >
            다음
          </button>
        )}
      </div>
    </section>
  );
};
