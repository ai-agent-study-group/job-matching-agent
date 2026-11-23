const steps = ["이력서 제출", "프로필 추출", "공고 검색", "결과"];

export const MatchingSteps = ({ currentStep }: { currentStep: number }) => {
  return (
    <ol
      aria-label="매칭 진행 단계"
      className="grid grid-cols-2 gap-2 sm:grid-cols-4"
    >
      {steps.map((label, index) => {
        const stepNumber = index + 1;
        const isCurrent = stepNumber === currentStep;

        return (
          <li
            key={label}
            aria-current={isCurrent ? "step" : undefined}
            className={`rounded-md border p-3 text-sm ${
              isCurrent ? "border-primary bg-primary/10 font-semibold" : ""
            }`}
          >
            {stepNumber}. {label}
          </li>
        );
      })}
    </ol>
  );
};