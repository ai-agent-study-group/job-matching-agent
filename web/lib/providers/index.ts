import "server-only";
import { demoProvider } from "./demo";
export function getProvider() {
  if (process.env.AGENT_PROVIDER && process.env.AGENT_PROVIDER !== "demo")
    throw new Error("실제 AI 제공자는 아직 연결되지 않았습니다.");
  return demoProvider;
}
