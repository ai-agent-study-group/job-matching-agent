"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { CircleAlert, FileText } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";
import { RESUME_MAX_LENGTH, SAMPLE_RESUME } from "@/constants/profile";
import { resumeTextError } from "@/domain/profile/resume";
import { postProfile } from "@/lib/api/profile";
import { JobSearch } from "./JobSearch";
import { Loading } from "./Loading";
import { ProfileView } from "./ProfileView";

export const ProfileUpload = () => {
  const [text, setText] = useState(SAMPLE_RESUME);
  const [file, setFile] = useState<File | null>(null);
  const { mutate, data, error, isPending, submittedAt } = useMutation({
    mutationFn: postProfile,
  });

  const resume = file ?? text.trim();
  // 보낼 가치가 없는 글은 LLM을 부르기 전에 막음. 파일은 BE가 검사
  const textError = file ? null : resumeTextError(text);

  return (
    <div className="grid items-start gap-6 lg:grid-cols-3">
      {/* 입력: 모바일은 위, 넓은 화면은 오른쪽 */}
      <aside className="soft-card p-5 lg:sticky lg:top-20 lg:order-2">
        <form
          className="grid gap-3"
          onSubmit={(e) => {
            e.preventDefault();
            if (!textError) mutate(resume);
          }}
        >
          <h2 className="text-base font-semibold">이력서 입력</h2>
          <div className="grid gap-1.5">
            <label htmlFor="resume-text" className="text-sm font-medium">
              이력서 글
            </label>
            <p className="text-xs text-muted-foreground">
              예시 이력서가 들어 있습니다. 지우고 내 이력서를 붙여 넣으세요.
            </p>
            <Textarea
              id="resume-text"
              rows={10}
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={!!file}
              placeholder="이력서 내용을 붙여 넣으세요"
              className="text-sm"
              aria-invalid={!!textError}
              aria-describedby="resume-text-status"
            />
            <div
              id="resume-text-status"
              className="flex justify-between gap-3 text-xs"
            >
              <p className="text-destructive" aria-live="polite">
                {textError}
              </p>
              <p className="shrink-0 text-muted-foreground tabular-nums">
                {text.trim().length.toLocaleString("ko-KR")} /{" "}
                {RESUME_MAX_LENGTH.toLocaleString("ko-KR")}자
              </p>
            </div>
          </div>
          <div className="grid gap-1.5">
            <label
              htmlFor="resume-file"
              className="flex items-center gap-2 text-sm font-medium"
            >
              또는 파일 (PDF · DOCX)
              <Badge variant="secondary">준비 중</Badge>
            </label>
            <Input
              id="resume-file"
              type="file"
              accept=".pdf,.docx"
              // ponytail: BE가 파일을 아직 415로 막음. #44에서 route에 파서를 붙이면 disabled를 지움
              disabled
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
          </div>
          <Button
            type="submit"
            disabled={!!textError || isPending}
            className="rounded-full"
          >
            {isPending && <Spinner />}
            프로필 만들기
          </Button>
        </form>
        {error && (
          <Alert variant="destructive" className="mt-4">
            <CircleAlert aria-hidden />
            <AlertTitle>요청 실패</AlertTitle>
            <AlertDescription>{error.message}</AlertDescription>
          </Alert>
        )}
      </aside>

      <div className="grid gap-3 lg:order-1 lg:col-span-2">
        {isPending && (
          <div className="soft-card">
            <Loading title="이력서를 분석하는 중" />
          </div>
        )}
        {!isPending && data && (
          <>
            <ProfileView profile={data} />
            {/* 새 프로필이 오면 지난 검색 결과를 지움 */}
            <JobSearch key={submittedAt} profile={data} />
          </>
        )}
        {!isPending && !data && (
          <div className="soft-card flex flex-col items-center gap-3 px-6 py-16 text-center">
            <FileText className="size-10 text-muted-foreground" aria-hidden />
            <p className="text-lg font-semibold">아직 프로필이 없습니다</p>
            <p className="max-w-sm text-sm text-muted-foreground">
              이력서를 넣고 프로필 만들기를 누르면 경력 · 학력 · 기술을 정리해
              보여 줍니다.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
