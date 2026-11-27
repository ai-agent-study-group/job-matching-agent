import type { components } from "@/lib/api-types/api.generated";
import { throwIfFailed } from "./error";

type Profile = components["schemas"]["Profile-Output"];

/** 이력서(글 또는 PDF·DOCX 파일)를 보내 프로필을 받음. 실패하면 BE의 detail을 담아 throw */
export const postProfile = async (resume: string | File): Promise<Profile> => {
  const body = new FormData();
  body.append("resume", resume);
  const res = await fetch("/api/profile", { method: "POST", body });
  await throwIfFailed(res);
  return res.json();
};
