import { JobCard } from "./JobCard";

const jobs = [
  {
    id: "1",
    title: "Backend Engineer",
    company: "예시 기업 A",
    location: "서울",
    source: "예시 채용 게시판",
    url: "https://example.com/",
    description: "서비스 API를 개발하고 운영해요.",
  },
  {
    id: "2",
    title: "Data Engineer",
    company: "예시 기업 B",
    location: "원격",
    source: "예시 기업 채용 페이지",
    url: "https://example.com/",
  },
];

export const JobList = ({ showEmpty = false }: { showEmpty?: boolean }) => {
  const visibleJobs = showEmpty ? [] : jobs;

  return (
    <section className="space-y-4">
      <h2 className="text-xl font-semibold">채용 공고 · 예시</h2>

      {visibleJobs.length === 0 ? (
        <p>검색 결과가 없어요.</p>
      ) : (
        visibleJobs.map(({ id, ...job }) => <JobCard key={id} {...job} />)
      )}
    </section>
  );
};
