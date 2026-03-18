---
name: status
description: |
  cmux 사이드바 상태/알림 관리 - 진행률, 상태 표시, 알림, 로그.
  작업 진행률 표시, 상태 업데이트, 알림 전송, 로그 기록 등 사이드바 UI 제어가 필요할 때 사용합니다.
---

# cmux:status - 사이드바 상태/알림 관리

AI 에이전트의 작업 진행 상황을 사이드바에 시각적으로 전달합니다.

## 명령어 카테고리

| 카테고리 | 주요 명령어 | 용도 |
|----------|------------|------|
| 상태 표시 | `set-status`, `clear-status`, `list-status` | 키-값 상태 pill |
| 진행률 | `set-progress`, `clear-progress` | 진행률 바 (0.0~1.0) |
| 알림 | `notify`, `list-notifications`, `clear-notifications` | 시스템 알림 |
| 로그 | `log`, `list-log`, `clear-log` | 사이드바 로그 |
| 전체 조회 | `sidebar-state` | 모든 메타데이터 덤프 |

명령어 상세 옵션은 플러그인 루트의 `references/cli-reference.md`를 참조하세요.

## 주요 패턴

```bash
# 상태: cmux set-status <key> <value> [--icon <name>] [--color <#hex>]
cmux set-status build "compiling" --icon hammer --color "#ff9500"

# 진행률: cmux set-progress <0.0-1.0> [--label <text>]
cmux set-progress 0.75 --label "테스트 실행 (3/4)"

# 로그 레벨: info, progress, success, warning, error
cmux log --level success "빌드 완료"
```

## 주의사항

- `set-status`의 key는 고유 식별자로 동일 key에 대해 덮어쓰기됨
- `set-progress`의 값은 0.0~1.0 범위 (0% ~ 100%)
- 로그 레벨에 따라 사이드바에서 다른 색상/아이콘으로 표시됨
- 알림은 macOS 시스템 알림으로도 표시될 수 있음
