import Link from "next/link";
import { MapPin } from "lucide-react";
import { CompanyLogo } from "@/components/shared/CompanyLogo";
import { MOCK_CARD, MockAlert, MockBadge } from "@/components/shared/MockAlert";
import { countMet, formatScore } from "@/domain/match/labels";
import { IS_MOCK, getMatches } from "@/lib/api/match";
import { cn } from "@/utils/style";

export const metadata = { title: "매칭 결과" };

export default async function MatchesPage() {
  const matches = await getMatches();

  return (
    <main id="main" className="page-shell max-w-3xl py-6">
      {IS_MOCK && <MockAlert />}
      <section className={cn("soft-card", IS_MOCK && MOCK_CARD)}>
        <header className="border-b border-border p-5">
          <h1 className="text-xl font-semibold">매칭 결과</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            공고 {matches.length}건 · 적합도가 높은 순. 공고를 누르면 요건마다
            판정과 근거를 볼 수 있습니다.
          </p>
        </header>
        <ul className="divide-y divide-border">
          {matches.map(({ posting, result }) => (
            <li key={`${posting.source}/${posting.id}`}>
              <Link
                href={`/matches/${posting.source}/${encodeURIComponent(posting.id)}`}
                className="group flex gap-3 p-5 transition-colors hover:bg-muted"
              >
                <CompanyLogo name={posting.company} className="size-14" />
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="font-semibold text-primary group-hover:underline">
                      {posting.title}
                    </h2>
                    {IS_MOCK && <MockBadge />}
                  </div>
                  <p className="text-sm">{posting.company}</p>
                  <p className="flex items-center gap-1 text-sm text-muted-foreground">
                    <MapPin className="size-3.5" aria-hidden />
                    {posting.location}
                  </p>
                  <p className="mt-2 text-xs text-muted-foreground">
                    {result.checks.length}개 항목 중 {countMet(result.checks)}개
                    충족
                  </p>
                </div>
                <div className="shrink-0 text-right">
                  <p className="text-2xl font-semibold text-primary">
                    {formatScore(result.score)}
                  </p>
                  <p className="text-xs text-muted-foreground">적합도</p>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
