import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main id="main" className="page-shell py-12 sm:py-20">
      <section className="max-w-2xl">
        <p className="eyebrow mb-5">RESUME MATCHING</p>
        <h1 className="text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
          반복되는 구직,
          <br />
          공고를 찾아 이력서와 맞추는
          <br />
          <span className="text-primary">에이전트와 함께.</span>
        </h1>
        <p className="mt-6 max-w-md text-base leading-8 text-slate-500">
          이력서를 올리면 경력·기술을 정리한 프로필을 만들어 드립니다. 이
          프로필로 채용공고와 비교해 강점과 보완할 점을 확인하세요.
        </p>
        <Button asChild className="mt-7 h-auto rounded-full px-6 py-3 text-sm">
          <Link href="/profile">
            이력서 올리기 <ArrowRight size={16} />
          </Link>
        </Button>
      </section>
    </main>
  );
}
