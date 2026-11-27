import type { NextConfig } from "next";

// BE에 CORS가 없어서 /api 요청을 Next가 BE로 넘김 (같은 출처)
const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  typedRoutes: true,
  experimental: {
    // LLM 응답이 30초(Next 프록시 기본값)를 넘기도 해서 넘으면 socket hang up · 500이 남. 공고 검색은 더 오래 걸림
    proxyTimeout: 120_000,
  },
  rewrites: async () => [
    { source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` },
  ],
};

export default nextConfig;
