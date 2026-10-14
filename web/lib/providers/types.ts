import type { Domain, Source, SourceHit, Turn } from "@/lib/types";
import type { toolDefinitions } from "@/lib/tools/sources";
export interface ToolRequest {
  type: "tool_call";
  callId: string;
  name: string;
  arguments: unknown;
}
export interface ToolResult {
  request: ToolRequest;
  ok: boolean;
  value?: SourceHit[] | Source;
  error?: string;
}
export interface ProviderInput {
  domain: Domain;
  instructions: string;
  messages: Turn[];
  tools: typeof toolDefinitions;
  toolResults: ToolResult[];
}
export type ModelDecision =
  | ToolRequest
  | { type: "answer"; text: string; sourceIds: string[] };
export interface ModelProvider {
  mode: "demo";
  decide(input: ProviderInput): Promise<ModelDecision>;
}
// 실제 제공자를 연결하면 mode에 "live"를 추가하고 UI/API 표시도 함께 갱신하세요.
// 도구 요청의 callId, 인자, 결과를 해당 모델의 메시지 형식으로 변환하는 어댑터를 구현합니다.
