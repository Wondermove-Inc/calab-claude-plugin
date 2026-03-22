---
name: workspace
description: |
  cmux 워크스페이스/패널 관리 - 생성, 분할, 텍스트 전송, 터미널 캡처.
  터미널 분할, 새 워크스페이스 생성, 패널 관리, 터미널 캡처, cmux send 등 터미널 멀티플렉서 작업이 필요할 때 사용합니다.
allowed-tools: Bash
---

# cmux:workspace - 워크스페이스/패널 관리

계층: Window → Workspace → Pane → Surface (Terminal | Browser)

## 명령어 카테고리

| 카테고리 | 주요 명령어 | 용도 |
|----------|------------|------|
| 워크스페이스 | `list-workspaces`, `new-workspace`, `select-workspace`, `close-workspace` | 워크스페이스 CRUD |
| 패널 분할 | `new-split`, `new-pane`, `list-panes`, `focus-pane` | 화면 분할/포커스 |
| 텍스트 전송 | `send`, `send-key` | 터미널에 명령 전송 |
| 터미널 캡처 | `capture-pane`, `read-screen` | 터미널 출력 읽기 |
| 계층 조회 | `tree`, `identify`, `surface-health` | 구조/상태 확인 |

명령어 상세 옵션은 플러그인 루트의 `references/cli-reference.md`를 참조하세요.

## 주의사항

- ID 참조 형식: UUID, 짧은 ref (`workspace:1`), 인덱스 사용 가능
- cmux 환경 내에서는 `CMUX_WORKSPACE_ID`가 자동 설정되어 `--workspace` 생략 가능
- `cmux send`로 전송된 텍스트는 실제 터미널 입력과 동일하게 동작
- 패널 분할 후 새 패널에 포커스가 이동됨
