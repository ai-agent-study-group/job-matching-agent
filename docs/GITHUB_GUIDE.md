# 문서 작성과 로컬 미리보기

Markdown 문서는 GitHub 저장소 화면에서 읽고 만들고 수정할 수 있습니다.
문서 협업을 위한 별도 웹사이트 배포는 필요하지 않습니다. 저장소에 파일이 올라가고 참여자에게 필요한 접근 권한이 있어야 합니다.
이 안내를 작성한 것과 실제 저장소 업로드·권한 설정을 완료한 것은 별개입니다.

## 배포 전에 로컬에서 확인하기

프로젝트 루트에서 Node.js 20 이상과 npm을 사용합니다. 문서 미리보기 도구이며 앱의 BE 언어 선택과는 별개입니다.

```bash
npm install
npm run docs:dev
```

브라우저에서 [http://localhost:4174](http://localhost:4174)을 엽니다.
`docs/`의 Markdown이나 `index.html`을 저장하면 화면이 자동으로 새로고침됩니다.
새 회의록이나 문서를 추가한 경우도 포함합니다. 로컬 확인에는 커밋·푸시·배포가 필요하지 않습니다.
한 번 설치한 뒤에는 `npm run docs:dev`만 실행하면 됩니다. 종료는 터미널에서 `Ctrl+C`입니다.

4174 포트가 사용 중이면 다른 포트를 지정할 수 있습니다.

```bash
# macOS / Linux
DOCS_PORT=4175 npm run docs:dev
```

Windows PowerShell에서는 `$env:DOCS_PORT=4175`를 실행한 뒤 `npm run docs:dev`를 실행합니다.

`index.html`은 Markdown을 포함하는 Liquid 문법을 사용하므로 파일을 더블클릭하거나 단순 파일 서버로 여는 것만으로는 문서 메뉴가 완성되지 않습니다.
미리보기 명령은 로컬 파일을 변환해 보여줍니다. 실제 배포의 Jekyll과 미리보기의 Markdown 변환기는 달라 세부 서식에는 차이가 있을 수 있습니다.

## 문서가 보이는 시점

| 확인하는 곳 | 변경을 보는 방법 |
| --- | --- |
| 로컬 `localhost:4174` | 파일을 저장하면 자동 반영 |
| GitHub 저장소 | 변경을 커밋·푸시하거나 웹에서 저장한 뒤 확인 |
| 공개 GitHub Pages URL | 배포 대상 브랜치에 반영되고 배포가 완료된 뒤 확인 |

## 기존 문서 수정

1. GitHub에서 저장소를 열고 수정할 `.md` 파일을 선택합니다.
2. 연필 모양의 편집 버튼으로 내용을 수정합니다.
3. `Preview`에서 표·링크·줄바꿈을 확인합니다.
4. `Commit changes`에서 수정 내용을 설명합니다.
5. 새 브랜치를 만들어 PR을 여는 선택지를 사용합니다. 예: `docs/meeting-2026-10-20`.
6. PR에서 팀원이 내용을 확인하고, 저장소의 리뷰·검사 조건에 맞게 병합합니다.

브랜치는 원본과 별도로 변경을 준비하는 공간이고, PR은 그 변경을 함께 검토하는 요청입니다.
문서 변경에도 기존 [기여 규칙](https://github.com/ai-agent-study-group/job-matching-agent/blob/main/CONTRIBUTING.md)의 PR 절차를 적용합니다.

## 새 회의록 만들기

1. [회의록 템플릿](meetings/TEMPLATE.md)을 열고 본문을 복사합니다.
2. 저장소에서 `Add file → Create new file`을 선택합니다.
3. 파일 이름에 `docs/meetings/YYYY-MM-DD.md`를 입력합니다.
4. 본문을 붙여넣고 날짜·안건을 작성합니다. 미정 내용은 빈칸이나 `?`로 둡니다.
5. 미리보기를 확인하고 새 브랜치·PR로 변경을 제안합니다.
6. 같은 브랜치에서 `docs/meetings/README.md`의 목록에도 회의록 링크를 추가합니다.

폴더 경로와 파일 이름을 함께 입력해 새 폴더 안의 파일도 만들 수 있습니다.
여러 파일을 함께 수정할 때는 GitHub의 `github.dev` 웹 편집기를 활용할 수도 있습니다.

## 회의 중·후 기록

참여자 목록은 제공되지 않아 기재하지 않았습니다. 계정·배경·현재 활동·연락처·개인별 제공 정보는 기록하지 않습니다. 작업의 담당은 역할명으로 표시합니다.

- 의견·후보는 논의 메모, 합의한 내용은 결정 사항에 기록합니다.
- 담당자·기한·다음 일정도 합의한 내용만 채웁니다.
- 여러 명이 같은 문서를 편집한다면 회의 기록자를 정하거나 수정할 부분을 나누는 방식을 논의할 수 있습니다.
- 회의 이후 같은 PR에서 기록을 보완하고, 확정된 내용을 프로젝트·역할 문서에 반영할 수 있습니다.

## 저장소 관리자와 확인할 것

| 항목 | 확인 내용 |
| --- | --- |
| 저장소 주소·공개 범위 | ? |
| 참여자 초대·쓰기 권한 | ? |
| 문서 리뷰·병합 담당 | ? |
| 브랜치 보호·필수 검사 | 실제 GitHub 설정은 ? |

쓰기 권한이 없으면 포크와 PR로 제안할 수 있지만, 비공개 저장소는 접근 권한과 포크 정책도 확인해야 합니다.

GitHub Pages는 문서를 별도 정적 사이트로 보여주고 싶을 때 검토할 수 있습니다.
이것과 실제 agent 웹앱·API의 배포 환경 선택은 각각 별도 논의 항목입니다.

## 공식 안내

- [파일 수정](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
- [파일 생성](https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files)
- [PR 시작하기](https://docs.github.com/en/pull-requests/get-started/pull-request-quickstart)
- [GitHub 웹 편집기](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)
- [GitHub Pages 소개](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## 현재 문서 사이트 배포

저장소 `Settings → Pages`에서 다음 구성을 사용하는 경우를 위한 설정입니다.

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`

접속 주소: [스터디 문서](https://ai-agent-study-group.github.io/job-matching-agent/)
`docs/`는 배포 원본 폴더이므로 접속 주소 뒤에 `/docs/`를 붙이지 않습니다.

`docs/index.html` 하나가 첫 화면·메뉴·스타일·문서 전환을 담당합니다.
GitHub Pages 기본 Jekyll 빌드가 Markdown 문서를 HTML 안에 포함하므로 별도 설정 파일이나 외부 라이브러리가 필요하지 않습니다.
이 방식은 `Deploy from a branch`의 `/docs` 배포를 기준으로 하며, 파일을 그대로 복사하는 배포에서는 Jekyll 빌드가 필요합니다.

메뉴는 공통 필독 → 역할별 읽기 → 회의 기록 → 설계·추가 문서 → 저장소 안내 순서입니다.
역할별 읽기는 담당자 배정이 아니라 참고 문서를 읽는 순서입니다. 역할 안내 화면도 `index.html` 안에 있습니다.

새 문서는 `docs/`에 일반 `.md` 파일로 추가하면 됩니다. 별도의 front matter는 필요하지 않습니다.
파일의 첫 제목을 `# 문서 제목`으로 작성하면 메뉴 제목으로 사용됩니다.
회의록은 `docs/meetings/`에서 최신 날짜순으로, 그 외 새 문서는 추가 문서 영역에 자동 표시됩니다.
공통 필독·역할별 읽기에 넣을 문서는 `index.html`의 해당 링크를 편집하면 됩니다.

메뉴에서 문서를 선택하면 같은 화면에서 내용이 바뀌고, 문서별 URL을 복사해 공유할 수 있습니다.
Markdown 안에서 다른 Markdown 문서로 이동하는 링크도 같은 화면에서 열립니다.
`docs/` 밖의 문서는 GitHub 링크로 확인합니다.

변경이 `main`에 반영된 뒤 Pages 배포가 완료되어야 사이트에 표시됩니다.
