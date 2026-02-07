---
name: statusline
description: Claude Code statusline 설치. 터미널에 모델명, 컨텍스트 사용량, Git 상태를 표시합니다.
allowed-tools: Bash, Read, Write, AskUserQuestion
disable-model-invocation: true
---

# /setup:statusline - Statusline 설치

## 설명
Claude Code 터미널에 상태 정보를 표시하는 statusline을 설치합니다.

## 사용법
- `/setup:statusline` - 플러그인 statusline 설치

## Statusline 표시 정보
```
[Opus 4.5] ██████░░░░ 60% | ➜ my-project git:(main)
```

- **모델명**: 현재 사용 중인 Claude 모델
- **컨텍스트 게이지**: 10칸 진행바 + 백분율
- **디렉토리**: 현재 작업 폴더명
- **Git 상태**: 브랜치명, 변경사항 표시 (✗)

### 색상 규칙
- 녹색: 50% 미만 (안전)
- 노란색: 50-75% (주의)
- 빨간색: 75% 이상 (위험)

---

## 설치 모드

### 1단계: 현재 상태 확인
```bash
# 현재 설정 확인
cat ~/.claude/settings.json 2>/dev/null | grep -A5 statusLine || echo "statusLine 설정 없음"
ls -la ~/.claude/statusline-command.sh 2>/dev/null || echo "스크립트 없음"
```

### 2단계: 사전 요구사항 확인
```bash
which jq || echo "jq 미설치"
which bc || echo "bc 미설치"
```

### 3단계: 설치 확인
사용자에게 설치 진행 여부를 확인합니다.

### 4단계: 설치 실행
```bash
bash {PLUGIN_PATH}/scripts/setup-statusline.sh
```

### 5단계: 검증 및 완료
```bash
echo '{"model":{"display_name":"Claude Opus 4.5"},"workspace":{"current_dir":"'$(pwd)'"},"context_window":{"remaining_percentage":40,"used_percentage":60}}' | bash ~/.claude/statusline-command.sh
```
설치 완료 후 Claude Code 재시작을 안내합니다.

---

## 문제 해결

### jq 미설치
- macOS: `brew install jq`
- Ubuntu/Debian: `sudo apt install jq`

### bc 미설치 (Linux)
- Ubuntu/Debian: `sudo apt install bc`
