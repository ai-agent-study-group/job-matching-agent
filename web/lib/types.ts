export type Domain = "backend" | "data";
export interface Source {
  id: string;
  domain: Domain;
  title: string;
  body: string;
  url: string;
  keywords: string[];
  collectedAt: string;
  reviewedAt: string;
  reviewed: boolean;
  language: string;
  kind: "editorial_summary" | "scraped";
}
export interface SourceHit {
  id: string;
  title: string;
  excerpt: string;
  score: number;
}
export interface Citation {
  id: string;
  title: string;
  url: string;
  reviewedAt: string;
  kind: Source["kind"];
}
export interface Turn {
  role: "user" | "assistant";
  content: string;
}
export interface Activity {
  type: "search" | "read" | "answer" | "error" | "limit";
  label: string;
  detail: string;
}
export interface ChatResult {
  mode: "demo";
  answer: string;
  citations: Citation[];
  activities: Activity[];
}
