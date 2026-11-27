// BE detail은 영어라 상태 코드로 한국어 문구를 고름 (BE: src/adapter/inbound/api/error.py · route.py)
const MESSAGES: Record<number, string> = {
  415: "이력서 파일은 아직 지원하지 않습니다. 이력서 내용을 글로 붙여 넣어 주세요.",
  422: "보낸 내용이 올바르지 않습니다. 입력을 확인해 주세요.",
  500: "서버 응답을 받지 못했습니다. 백엔드가 켜져 있는지 확인하고 다시 시도해 주세요.",
  502: "AI 처리 중 오류가 났습니다. 다시 시도해 주세요.",
  503: "AI 요청이 많아 처리하지 못했습니다. 잠시 뒤 다시 시도해 주세요.",
  504: "AI 응답이 너무 늦습니다. 잠시 뒤 다시 시도해 주세요.",
};

/** 응답이 실패면 상태 코드에 맞는 한국어 문구로 throw */
export const throwIfFailed = async (res: Response) => {
  if (res.ok) return;
  throw new Error(
    MESSAGES[res.status] ?? `요청에 실패했습니다 (${res.status}).`,
  );
};
