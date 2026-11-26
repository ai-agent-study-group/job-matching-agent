type ProfileSummaryProps = {
  jobTitles: string[];
  locations: string[];
};

export const ProfileSummary = ({
  jobTitles,
  locations,
}: ProfileSummaryProps) => {
  return (
    <section className="space-y-4 rounded-xl border p-6">
      <h2 className="text-lg font-semibold">이력서 요약 · 예시</h2>

      <div>
        <h3 className="font-medium">희망 직무</h3>
        <p className="text-muted-foreground">
          {jobTitles.length > 0
            ? jobTitles.join(" · ")
            : "표시할 직무가 없어요."}
        </p>
      </div>

      <div>
        <h3 className="font-medium">희망 근무지</h3>
        <p className="text-muted-foreground">
          {locations.length > 0
            ? locations.join(" · ")
            : "표시할 근무지가 없어요."}
        </p>
      </div>
    </section>
  );
};
