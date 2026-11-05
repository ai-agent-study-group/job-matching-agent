"use client";

import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

/** 전역 클라이언트 Provider — 서버 데이터 캐싱(React Query). 루트 레이아웃에서 감싼다. */
export const Providers = ({ children }: { children: React.ReactNode }) => {
  // 요청별 QueryClient (서버에서 상태 공유 방지)
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};
