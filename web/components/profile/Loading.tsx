import { Spinner } from "@/components/ui/spinner";

/** LLM을 기다리는 동안 띄우는 큰 스피너. 응답이 수십 초 걸릴 수 있어 안내를 같이 보여 줌 */
export const Loading = ({ title }: { title: string }) => (
  <div
    role="status"
    className="flex flex-col items-center gap-3 px-6 py-16 text-center"
  >
    <Spinner className="size-10 text-primary" role="presentation" aria-hidden />
    <p className="text-lg font-semibold">{title}</p>
    <p className="text-sm text-muted-foreground">
      AI가 처리하고 있습니다. 1분 가까이 걸릴 수 있습니다.
    </p>
  </div>
);
