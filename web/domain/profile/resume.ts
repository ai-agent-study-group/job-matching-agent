import { RESUME_MAX_LENGTH, RESUME_MIN_LENGTH } from "@/constants/profile";

/** 이력서 글을 보내기 전에 검사. 문제가 없으면 null, 있으면 화면에 띄울 문구 */
export const resumeTextError = (text: string): string | null => {
  const length = text.trim().length;
  if (length === 0) return "이력서 내용을 붙여 넣어 주세요.";
  if (length < RESUME_MIN_LENGTH)
    return `이력서 내용이 너무 짧습니다. ${RESUME_MIN_LENGTH}자 이상 넣어 주세요.`;
  if (length > RESUME_MAX_LENGTH)
    return `이력서 내용이 너무 깁니다. ${RESUME_MAX_LENGTH.toLocaleString("ko-KR")}자 이하로 줄여 주세요.`;
  return null;
};
