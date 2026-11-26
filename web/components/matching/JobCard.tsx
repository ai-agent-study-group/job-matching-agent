type JobCardProps = {
  title: string;
  company: string;
  location: string;
  source: string;
  url: string;
  description?: string;
};

export const JobCard = ({
  title,
  company,
  location,
  source,
  url,
  description,
}: JobCardProps) => {
  return (
    <article className="space-y-2 rounded-xl border p-6">
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-sm text-muted-foreground">
        {company} · {location}
      </p>
      <p className="text-sm text-muted-foreground">출처: {source}</p>
      <p>{description?.trim() || "공고 설명이 없어요."}</p>
      <a href={url} className="inline-block text-sm underline">
        {title} 공고 원문 (예시 링크)
      </a>
    </article>
  );
};
