import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, MapPin } from "lucide-react";
import { VerdictBadge } from "@/components/match/VerdictBadge";
import {
  KIND,
  countMet,
  formatScore,
  groupByKind,
} from "@/domain/match/labels";
import { CompanyLogo } from "@/components/shared/CompanyLogo";
import { MOCK_CARD, MockAlert, MockBadge } from "@/components/shared/MockAlert";
import { IS_MOCK, getMatch } from "@/lib/api/match";
import { cn } from "@/utils/style";

type Params = Promise<{ source: string; id: string }>;

export const generateMetadata = async ({ params }: { params: Params }) => {
  const { source, id } = await params;
  const match = await getMatch(source, decodeURIComponent(id));
  return { title: match ? match.posting.title : "매칭 결과" };
};

export default async function MatchDetailPage({ params }: { params: Params }) {
  const { source, id } = await params;
  const match = await getMatch(source, decodeURIComponent(id));
  if (!match) notFound();
  const { posting, result } = match;

  return (
    <main id="main" className="page-shell max-w-3xl py-6">
      {IS_MOCK && <MockAlert />}
      <Link
        href="/matches"
        className="mb-3 inline-flex items-center gap-1 text-sm font-semibold text-muted-foreground hover:text-primary"
      >
        <ArrowLeft size={16} aria-hidden /> 매칭 결과
      </Link>

      <section className={cn("soft-card p-6", IS_MOCK && MOCK_CARD)}>
        <div className="flex items-start gap-4">
          <CompanyLogo name={posting.company} className="size-16" />
          <div className="min-w-0 flex-1">
            <p className="text-sm">{posting.company}</p>
            <h1 className="mt-0.5 text-2xl font-semibold">{posting.title}</h1>
            <p className="mt-1 flex items-center gap-1 text-sm text-muted-foreground">
              <MapPin className="size-3.5" aria-hidden />
              {posting.location}
            </p>
            {IS_MOCK && (
              <div className="mt-2">
                <MockBadge />
              </div>
            )}
          </div>
          <div className="shrink-0 text-right">
            <p className="text-3xl font-semibold text-primary">
              {formatScore(result.score)}
            </p>
            <p className="text-xs text-muted-foreground">적합도</p>
          </div>
        </div>
        <p className="mt-4 border-t border-border pt-4 text-sm text-muted-foreground">
          {result.checks.length}개 항목 중 {countMet(result.checks)}개 충족
        </p>
      </section>

      <div className="mt-3 grid gap-3">
        {groupByKind(result.checks).map((group) => (
          <section key={group.kind} className="soft-card p-6">
            <h2 className="mb-2 text-xl font-semibold">{KIND[group.kind]}</h2>
            <ul className="divide-y divide-border">
              {group.checks.map((c, i) => (
                <li key={i} className="flex items-start gap-3 py-3 last:pb-0">
                  <VerdictBadge verdict={c.verdict} />
                  <div className="min-w-0 text-sm">
                    <p className="font-medium">{c.target}</p>
                    {c.evidence && (
                      <blockquote className="mt-2 rounded-md bg-muted px-3 py-2 text-muted-foreground">
                        <span className="sr-only">근거가 된 이력서 문장: </span>
                        {c.evidence}
                      </blockquote>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </main>
  );
}
