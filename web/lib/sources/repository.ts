import "server-only";
import { readFile } from "node:fs/promises";
import path from "node:path";
import type { Domain, Source } from "@/lib/types";
export interface SourceRepository {
  list(domain: Domain): Promise<Source[]>;
}
export function validSource(value: unknown, domain: Domain): value is Source {
  if (!value || typeof value !== "object") return false;
  const s = value as Source;
  return (
    s.domain === domain &&
    /^[a-z0-9-]+$/.test(s.id) &&
    typeof s.title === "string" &&
    typeof s.body === "string" &&
    s.body.length > 0 &&
    typeof s.url === "string" &&
    s.url.startsWith("https://") &&
    s.reviewed === true &&
    /^\d{4}-\d{2}-\d{2}/.test(s.reviewedAt) &&
    typeof s.collectedAt === "string" &&
    typeof s.language === "string" &&
    ["editorial_summary", "scraped"].includes(s.kind) &&
    Array.isArray(s.keywords) &&
    s.keywords.every((k) => typeof k === "string")
  );
}
// 이후 서버/DB를 쓰면 이 저장소 구현만 교체합니다.
export const localRepository: SourceRepository = {
  async list(domain) {
    const data: unknown = JSON.parse(
      await readFile(
        path.join(process.cwd(), "data", `${domain}.json`),
        "utf8",
      ),
    );
    if (!Array.isArray(data)) throw new Error("자료 파일은 배열이어야 합니다.");
    return data.filter((s) => validSource(s, domain));
  },
};
