# 기여 규칙

## 브랜치

- main에서 분기
- 이름: `<type>/<짧은-설명>` (예: `feat/greenhouse-adapter`)
- type: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## PR

- main 직접 푸시 금지. 모든 변경은 PR로
- 병합 조건: 승인 1명 이상, CI 통과, 최신 main 기준 (up to date)
- 승인 후 새 커밋이 올라오면 승인 무효, 다시 리뷰
- 크기: 변경 400줄 이하 권장. 넘으면 나눠서 올림
- PR 템플릿 항목을 모두 채움

## 히스토리

PR마다 가지 하나, 가지끼리 겹치지 않는 모양 (semi-linear history).

```
main: A───────M1──────M2
       \     /  \     /
        B───C    D───E
```

- 브랜치는 최신 main에서 분기
- PR 올리기 전, 그리고 main이 바뀌어 병합이 막히면 최신 main 위로 rebase

  ```bash
  git fetch origin && git rebase origin/main
  git push --force-with-lease
  ```

- 브랜치에 main이나 다른 브랜치를 merge하지 않음 (GitHub의 "Update branch"는 "Update with rebase"로)
- 병합은 "Create a merge commit"만 사용 (squash, rebase 병합은 꺼져 있음)
- 남과 같이 쓰는 브랜치는 rebase 금지
- force push는 `--force-with-lease`로, 자기 브랜치에만

## 설명할 수 있는 코드

- AI 도구 사용 허용
- 작성자가 직접 읽고 동작을 설명할 수 없는 코드는 올리지 않음
- 바이브 코딩 결과를 그대로 푸시 금지
- PR 설명의 "무엇을, 왜"는 작성자가 직접 작성

## 리뷰

- 리뷰어는 이해가 안 되는 부분을 질문할 수 있음
- 작성자가 설명하지 못하면 승인하지 않음
