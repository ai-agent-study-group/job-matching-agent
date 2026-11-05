import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Tailwind 클래스 병합 (조건부 클래스 + 충돌 해결). shadcn `cn` 별칭. */
export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs));
