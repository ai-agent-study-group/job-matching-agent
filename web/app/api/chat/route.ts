import { isDomain } from "@/lib/agents/domains";
import { runAgent } from "@/lib/agents/run";
import type { Turn } from "@/lib/types";
export const runtime = "nodejs";
export async function POST(request: Request) {
  if (Number(request.headers.get("content-length")) > 30000)
    return Response.json({ error: "요청이 너무 큽니다." }, { status: 413 });
  let body;
  try {
    const raw = await request.text();
    if (raw.length > 30000)
      return Response.json({ error: "요청이 너무 큽니다." }, { status: 413 });
    body = JSON.parse(raw);
  } catch {
    return Response.json(
      { error: "올바른 요청을 보내주세요." },
      { status: 400 },
    );
  }
  if (
    !body ||
    typeof body !== "object" ||
    !isDomain(body.domain) ||
    !Array.isArray(body.messages) ||
    !body.messages.length ||
    body.messages.length > 12
  )
    return Response.json(
      { error: "분야와 대화 내용을 확인해주세요." },
      { status: 400 },
    );
  const turns: Turn[] = [];
  for (const [i, t] of body.messages.entries()) {
    if (
      !t ||
      t.role !== (i % 2 === 0 ? "user" : "assistant") ||
      typeof t.content !== "string" ||
      !t.content.trim() ||
      t.content.length > 2000
    )
      return Response.json(
        {
          error:
            "대화 형식이 올바르지 않습니다. 질문은 2,000자 이내로 입력해주세요.",
        },
        { status: 400 },
      );
    turns.push({ role: t.role, content: t.content.trim() });
  }
  if (turns.at(-1)?.role !== "user")
    return Response.json(
      { error: "마지막 메시지는 사용자 질문이어야 합니다." },
      { status: 400 },
    );
  try {
    return Response.json(await runAgent(body.domain, turns));
  } catch {
    return Response.json(
      { error: "자료 또는 제공자 설정을 확인해주세요." },
      { status: 503 },
    );
  }
}
