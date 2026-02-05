---
name: dev:setup
description: dev 플러그인의 워크플로우 강제 Hook을 사용자 설정(~/.claude/settings.json)에 설치합니다.
user-invocable: true
---

# /dev:setup 커맨드

dev 플러그인의 워크플로우 강제 Hook을 설치합니다.

## 설치 작업

다음 단계를 순서대로 수행하세요:

### 1단계: Hook 스크립트 복사

플러그인의 `workflow-guard.py`를 전역 hooks 폴더로 복사합니다.

```bash
mkdir -p ~/.claude/hooks
cp ~/.claude/plugins/cache/calab-marketplace/dev/*/hooks/workflow-guard.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/workflow-guard.py
```

### 2단계: 현재 설정 확인

```bash
cat ~/.claude/settings.json 2>/dev/null || echo "{}"
```

### 3단계: Hook 설정 추가

`~/.claude/settings.json` 파일을 읽고, `hooks.UserPromptSubmit` 배열에 다음 항목을 추가하세요:

```json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "python3 ~/.claude/hooks/workflow-guard.py \"$PROMPT\""
    }
  ]
}
```

**주의사항:**
- 파일이 없으면 새로 생성
- `hooks` 키가 없으면 추가
- `UserPromptSubmit` 배열이 없으면 추가
- 이미 workflow-guard 관련 hook이 있으면 중복 추가하지 않음

### 4단계: 결과 출력

설치 완료 후 다음 형식으로 결과를 출력:

```
✅ dev 플러그인 Hook 설치 완료

설치된 파일:
- ~/.claude/hooks/workflow-guard.py

설정 위치:
- ~/.claude/settings.json

적용된 기능:
- 개발 관련 요청 시 자동으로 /dev:workflow 호출
- 감지 키워드: 리팩토링, 기능 개발, 버그 수정, 최적화, 테스트, 설계

Hook을 제거하려면: /dev:setup --uninstall
```

## 제거 (--uninstall)

인자로 `--uninstall`이 전달되면:

1. `~/.claude/hooks/workflow-guard.py` 파일 삭제
2. `~/.claude/settings.json`에서 workflow-guard.py 관련 hook 항목 제거
3. 빈 배열이 되면 `UserPromptSubmit` 키 자체를 제거
4. 결과 출력:

```
✅ dev 플러그인 Hook 제거 완료

삭제된 파일:
- ~/.claude/hooks/workflow-guard.py

/dev:workflow 자동 호출이 비활성화되었습니다.
다시 설치하려면: /dev:setup
```
