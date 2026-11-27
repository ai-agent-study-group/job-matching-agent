import { GraduationCap, UserRound } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { CompanyLogo } from "@/components/shared/CompanyLogo";
import {
  formatDate,
  formatMonths,
  formatPeriod,
  languageLabel,
  languageLevelLabel,
  seniorityLabel,
  type Profile,
} from "@/domain/profile/labels";

const Empty = () => (
  <p className="text-sm text-muted-foreground">이력서에 없음</p>
);

const Section = ({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) => (
  <section className="soft-card p-6">
    <h2 className="mb-4 text-xl font-semibold">{title}</h2>
    {children}
  </section>
);

export const ProfileView = ({ profile }: { profile: Profile }) => (
  <div className="grid gap-3">
    {/* 상단 카드: 커버 · 아바타 · 헤드라인. 이름 · 연락처는 일부러 받지 않음 */}
    <section className="soft-card overflow-hidden">
      <div className="h-24 bg-linear-to-r from-sky-200 via-blue-200 to-indigo-200" />
      <div className="px-6 pb-6">
        <span className="-mt-12 flex size-24 items-center justify-center rounded-full border-4 border-card bg-slate-200 text-slate-500">
          <UserRound className="size-12" aria-hidden />
        </span>
        <p className="mt-3 text-2xl font-semibold">
          {seniorityLabel(profile.seniority)}
        </p>
        <p className="mt-1 text-muted-foreground">
          경력 {formatMonths(profile.months_of_experience)}
          {profile.experiences[0]?.company &&
            ` · ${profile.experiences[0].company}`}
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          {profile.languages.map((l) => (
            <Badge key={l.code} variant="secondary" className="rounded-full">
              {languageLabel(l.code)} · {languageLevelLabel(l.level ?? null)}
            </Badge>
          ))}
        </div>
      </div>
    </section>

    <Section title="경력">
      {profile.experiences.length === 0 && <Empty />}
      <ul className="divide-y divide-border">
        {profile.experiences.map((e, i) => (
          <li key={i} className="flex gap-3 py-4 first:pt-0 last:pb-0">
            <CompanyLogo name={e.company} />
            <div className="min-w-0">
              <h3 className="font-semibold">{e.title}</h3>
              {e.company && <p className="text-sm">{e.company}</p>}
              <p className="text-sm text-muted-foreground">
                {formatPeriod(e.start ?? null, e.end ?? null)}
              </p>
              {(e.highlights ?? []).length > 0 && (
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm">
                  {(e.highlights ?? []).map((h, j) => (
                    <li key={j}>{h.text}</li>
                  ))}
                </ul>
              )}
            </div>
          </li>
        ))}
      </ul>
    </Section>

    <Section title="학력">
      {profile.educations.length === 0 && <Empty />}
      <ul className="divide-y divide-border">
        {profile.educations.map((ed, i) => (
          <li key={i} className="flex gap-3 py-4 first:pt-0 last:pb-0">
            <span
              aria-hidden
              className="flex size-12 shrink-0 items-center justify-center rounded-md border border-border bg-slate-100 text-slate-500"
            >
              <GraduationCap className="size-5" />
            </span>
            <div>
              <h3 className="font-semibold">{ed.degree}</h3>
              {ed.subject && <p className="text-sm">{ed.subject}</p>}
              <p className="text-sm text-muted-foreground">
                {ed.end ? `${formatDate(ed.end)} 졸업` : "재학 중"}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </Section>

    <Section title="기술">
      {profile.skills.length === 0 && <Empty />}
      <div className="flex flex-wrap gap-2">
        {profile.skills.map((s) => (
          <Badge key={s} variant="outline" className="rounded-full px-3 py-1">
            {s}
          </Badge>
        ))}
      </div>
    </Section>
  </div>
);
