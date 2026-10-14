# resume-match-agent
- Git 작업은 사용자가 직접 수행한다. 요청 없이 git init, commit, push를 실행하지 않는다.
- 실제 AI 제공자는 아직 미정이다. 데모를 AI 생성 결과라고 표시하지 않는다.
- 채용공고 수집은 사이트 robots.txt·이용약관을 확인하고 공식 API를 우선한다. 차단을 우회하지 않는다.
- Next.js 변경 전 node_modules/next/dist/docs/의 해당 가이드를 읽는다.
- 공고 자료와 접근 키는 서버에서만 다룬다. 검토 대기 공고는 앱에서 읽지 않는다.
- 비개발자가 이해할 수 있는 한국어 설명을 사용한다.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
