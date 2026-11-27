"use client";

import { useMutation } from "@tanstack/react-query";
import { CircleAlert, Search } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { CompanyLogo } from "@/components/shared/CompanyLogo";
import type { Profile } from "@/domain/profile/labels";
import { postSearch } from "@/lib/api/search";
import { Loading } from "./Loading";

export const JobSearch = ({ profile }: { profile: Profile }) => {
  const { mutate, data, error, isPending } = useMutation({
    mutationFn: postSearch,
  });

  return (
    <section className="soft-card p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold">추천 공고</h2>
          <p className="text-sm text-muted-foreground">
            이 프로필로 채용공고를 찾습니다.
          </p>
        </div>
        <Button
          onClick={() => mutate(profile)}
          disabled={isPending}
          className="rounded-full"
        >
          {isPending ? <Spinner /> : <Search aria-hidden />}
          공고 찾기
        </Button>
      </div>

      {isPending && <Loading title="공고를 찾는 중" />}
      {error && (
        <Alert variant="destructive" className="mt-4">
          <CircleAlert aria-hidden />
          <AlertTitle>요청 실패</AlertTitle>
          <AlertDescription>{error.message}</AlertDescription>
        </Alert>
      )}
      {data?.length === 0 && (
        <p className="mt-4 text-sm text-muted-foreground">
          맞는 공고를 찾지 못했습니다.
        </p>
      )}
      {data && data.length > 0 && (
        <ul className="mt-4 divide-y divide-border border-t border-border">
          {data.map((p) => (
            <li key={`${p.source}/${p.id}`} className="flex gap-3 py-4">
              <CompanyLogo name={p.company} />
              <div className="min-w-0">
                <h3 className="font-semibold text-primary">{p.title}</h3>
                <p className="text-sm">{p.company}</p>
                <p className="text-sm text-muted-foreground">{p.location}</p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
};
