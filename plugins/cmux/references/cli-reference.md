# cmux CLI Reference (v0.62.2)

cmux는 Ghostty 기반 macOS 네이티브 터미널 멀티플렉서입니다.

## 계층 구조

```
Window → Workspace → Pane → Surface (Terminal | Browser)
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `CMUX_WORKSPACE_ID` | 현재 워크스페이스 ID (자동 설정) |
| `CMUX_SURFACE_ID` | 현재 서피스 ID (자동 설정) |
| `CMUX_SOCKET_PATH` | Unix 소켓 경로 (기본: ~/Library/Application Support/cmux/cmux.sock) |
| `CMUX_SOCKET_PASSWORD` | 소켓 인증 비밀번호 |

## ID 참조 형식

명령어에서 `<id|ref|index>` 파라미터는 다음 형식을 지원합니다:
- UUID: `a1b2c3d4-...`
- 짧은 ref: `workspace:1`, `pane:2`, `surface:3`
- 인덱스: `0`, `1`, `2`

## 글로벌 옵션

| 옵션 | 설명 |
|------|------|
| `--password` | 소켓 인증 비밀번호 |
| `--id-format uuids\|both` | ID 출력 형식 |

---

## Window 관리

```bash
cmux list-windows                                    # 창 목록
cmux new-window                                      # 새 창
cmux current-window                                  # 현재 창 ID
cmux focus-window --window <id|ref|index>            # 창 포커스
cmux close-window --window <id|ref|index>            # 창 닫기
cmux rename-window <title>                           # 창 이름 변경
```

## Workspace 관리

```bash
cmux list-workspaces                                 # 워크스페이스 목록
cmux new-workspace [--cwd <path>] [--command <text>] # 새 워크스페이스
cmux current-workspace                               # 현재 워크스페이스 ID
cmux select-workspace --workspace <id|ref|index>     # 워크스페이스 전환
cmux close-workspace --workspace <id|ref|index>      # 워크스페이스 닫기
cmux rename-workspace [--workspace <id|ref>] <title> # 이름 변경
cmux move-workspace-to-window --workspace <id|ref> --window <id|ref>  # 창 이동
cmux reorder-workspace [--workspace <id|ref>] (--index <n> | --before <id|ref> | --after <id|ref>)
```

### Workspace Actions

```bash
cmux workspace-action --action <name> [--workspace <id|ref>]
# actions: pin, unpin, rename, clear-name, move-up, move-down, move-top,
#          close-others, close-above, close-below, mark-read, mark-unread
```

## Pane 관리

```bash
cmux list-panes [--workspace <id|ref>]               # 패널 목록
cmux new-pane [--type <terminal|browser>] [--direction <left|right|up|down>] [--url <url>]
cmux focus-pane [--pane <id|ref>]                     # 패널 포커스
cmux new-split <left|right|up|down> [--workspace <id|ref>] [--surface <id|ref>]  # 패널 분할
cmux list-panels [--workspace <id|ref>]               # 패널(서피스) 목록
cmux focus-panel --panel <id|ref>                     # 패널 포커스
cmux resize-pane [--pane <id|ref>] (-L|-R|-U|-D) [--amount <n>]  # 크기 조절
cmux swap-pane --pane <id|ref> --target-pane <id|ref> # 패널 교체
cmux break-pane [--pane <id|ref>]                     # 독립 워크스페이스로 분리
cmux join-pane --target-pane <id|ref> [--pane <id|ref>]  # 패널 합치기
cmux last-pane                                        # 이전 패널로 포커스
```

## Surface 관리

```bash
cmux list-pane-surfaces [--pane <id|ref>]             # 서피스 목록
cmux new-surface [--type <terminal|browser>] [--pane <id|ref>] [--url <url>]  # 새 서피스 (탭)
cmux close-surface [--surface <id|ref>]               # 서피스 닫기
cmux move-surface [--surface <id|ref>] [--pane <id|ref>] [--before <id|ref>] [--after <id|ref>]
cmux reorder-surface [--surface <id|ref>] (--index <n> | --before <id|ref> | --after <id|ref>)
cmux rename-tab [--surface <id|ref>] <title>          # 탭 이름 변경
cmux drag-surface-to-split --surface <id|ref> <left|right|up|down>
```

### Tab Actions

```bash
cmux tab-action --action <name> [--tab <id|ref>]
# actions: rename, clear-name, close-left, close-right, close-others,
#          new-terminal-right, new-browser-right, reload, duplicate,
#          pin, unpin, mark-read, mark-unread
```

## 터미널 텍스트 전송

```bash
cmux send [--surface <id|ref>] <text>                 # 텍스트 전송 (\n, \r, \t 지원)
cmux send-key [--surface <id|ref>] <key>              # 키 이벤트 전송
cmux send-panel --panel <id|ref> <text>               # 패널에 텍스트 전송
cmux send-key-panel --panel <id|ref> <key>            # 패널에 키 전송
```

## 터미널 캡처

```bash
cmux capture-pane [--surface <id|ref>] [--scrollback] [--lines <n>]  # 터미널 텍스트 캡처
cmux read-screen [--surface <id|ref>] [--scrollback] [--lines <n>]   # 동일 기능
cmux clear-history [--surface <id|ref>]               # 스크롤백 삭제
cmux pipe-pane [--surface <id|ref>] [--command <shell-command>]      # 파이프
```

## 계층 조회

```bash
cmux tree [--all] [--workspace <id|ref>] [--json]     # 계층 트리
cmux identify [--workspace <id|ref>] [--surface <id|ref>] [--no-caller]  # 환경 정보
cmux surface-health [--workspace <id|ref>]             # 서피스 상태
cmux refresh-surfaces                                  # 스냅샷 갱신
```

## 사이드바 상태

```bash
cmux set-status <key> <value> [--icon <name>] [--color <#hex>]  # 상태 설정
cmux clear-status <key>                                # 상태 제거
cmux list-status                                       # 상태 목록
cmux set-progress <0.0-1.0> [--label <text>]           # 진행률 설정
cmux clear-progress                                    # 진행률 제거
cmux log [--level <level>] [--source <name>] <message> # 로그 기록
  # levels: info, progress, success, warning, error
cmux clear-log                                         # 로그 삭제
cmux list-log [--limit <n>]                            # 로그 조회
cmux sidebar-state                                     # 전체 사이드바 덤프
```

## 알림

```bash
cmux notify --title <text> [--subtitle <text>] [--body <text>]  # 알림 전송
cmux list-notifications                                # 알림 목록
cmux clear-notifications                               # 알림 삭제
```

## 버퍼 관리

```bash
cmux set-buffer [--name <name>] <text>                 # 버퍼 저장
cmux list-buffers                                      # 버퍼 목록
cmux paste-buffer [--name <name>] [--surface <id|ref>] # 버퍼 붙여넣기
```

## 유틸리티

```bash
cmux version                                           # 버전
cmux ping                                              # 연결 확인
cmux capabilities                                      # 서버 기능 (JSON)
cmux display-message [-p] <text>                       # 메시지 표시
cmux respawn-pane [--surface <id|ref>] [--command <cmd>]  # 셸 재시작
cmux find-window [--content] [--select] <query>        # 워크스페이스 검색
cmux wait-for [-S] <name> [--timeout <seconds>]        # 동기화 토큰
cmux markdown [open] <path>                            # 마크다운 미리보기
cmux themes list|set|clear                             # 테마 관리
```

## 워크스페이스 탐색

```bash
cmux next-window                                       # 다음 워크스페이스
cmux previous-window                                   # 이전 워크스페이스
cmux last-window                                       # 마지막 워크스페이스
```

## Hooks

```bash
cmux set-hook [--list] [--unset <event>] | <event> <command>
cmux trigger-flash [--surface <id|ref>]                # 읽지 않음 표시
```
