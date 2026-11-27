import { TriangleAlert } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";

const AMBER = "border-amber-300 bg-amber-50 text-amber-900";

/** 목 데이터를 보여 주는 화면 위에 띄우는 경고 */
export const MockAlert = () => (
  <Alert className={`mb-6 ${AMBER}`}>
    <TriangleAlert aria-hidden />
    <AlertTitle>목 데이터</AlertTitle>
    <AlertDescription className="text-amber-800">
      매칭 API가 아직 없어 예시 데이터를 보여 줍니다. 실제 이력서 · 공고와
      관계없습니다.
    </AlertDescription>
  </Alert>
);

/** 목 데이터 한 건 · 메뉴 옆에 붙이는 표시 */
export const MockBadge = () => (
  <Badge variant="outline" className={AMBER}>
    목 데이터
  </Badge>
);

/** 목 데이터 카드 테두리. soft-card 위에 덧씀 */
export const MOCK_CARD = "border-2 border-dashed border-amber-300";
