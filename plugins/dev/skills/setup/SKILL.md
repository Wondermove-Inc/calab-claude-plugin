---
name: dev:setup
description: |
  dev 플러그인의 워크플로우 강제 Hook을 사용자 설정에 설치합니다.
  설치 후 개발 관련 요청 시 자동으로 /dev:workflow가 호출됩니다.
---

# /dev:setup 커맨드

dev 플러그인의 워크플로우 강제 Hook을 `~/.claude/settings.json`에 설치합니다.

## 설치 작업

다음 단계를 순서대로 수행하세요:

### 1단계: 현재 설정 확인

```bash
cat ~/.claude/settings.json 2>/dev/null || echo "{}"
```

### 2단계: Hook 설정 추가

`~/.claude/settings.json` 파일을 읽고, `hooks.UserPromptSubmit` 배열에 다음 항목을 추가하세요:

```json
{
  "type": "command",
  "command": "python3 ~/.claude/plugins/cache/calab-marketplace/dev/*/hooks/workflow-guard.py \"$PROMPT\""
}
```

**주의사항:**
- 파일이 없으면 새로 생성
- `hooks` 키가 없으면 추가
- `UserPromptSubmit` 배열이 없으면 추가
- 이미 동일한 hook이 있으면 중복 추가하지 않음

### 3단계: 결과 출력

설치 완료 후 다음 형식으로 결과를 출력:

```
✅ dev 플러그인 Hook 설치 완료

설치 위치: ~/.claude/settings.json

적용된 기능:
- 개발 관련 요청 시 자동으로 /dev:workflow 호출
- 감지 키워드: 리팩토링, 기능 개발, 버그 수정, 최적화, 테스트, 설계

Hook을 제거하려면: /dev:setup --uninstall
```

## 제거 (--uninstall)

인자로 `--uninstall`이 전달되면:

1. `~/.claude/settings.json`에서 workflow-guard.py 관련 hook 항목 제거
2. 빈 배열이 되면 `UserPromptSubmit` 키 자체를 제거
3. 결과 출력:

```
✅ dev 플러그인 Hook 제거 완료

/dev:workflow 자동 호출이 비활성화되었습니다.
다시 설치하려면: /dev:setup
```
