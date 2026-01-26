---
name: cli-tools:setup
description: Claude Code statusline 자동 설치. 터미널에 모델명, 컨텍스트 사용량, git 상태를 표시합니다.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# /cli-tools:setup - Statusline 자동 설치

## 설명
Claude Code의 statusline을 자동으로 설치하여 터미널에 유용한 정보를 표시합니다.

## Statusline 표시 정보
- **모델명**: 현재 사용 중인 Claude 모델 (Opus, Sonnet, Haiku)
- **컨텍스트 사용량**: 진행바와 백분율로 표시
- **작업 디렉토리**: 현재 폴더명
- **Git 상태**: 브랜치명과 변경 여부

## 표시 예시
```
[Opus 4.5] ██████░░░░ 60% | ➜ my-project git:(main)
[Sonnet 4] ████░░░░░░ 40% | ➜ api-server git:(feature) ✗
```

- 컨텍스트 50% 미만: 녹색
- 컨텍스트 50-75%: 노란색
- 컨텍스트 75% 이상: 빨간색
- git 변경사항 있음: 빨간색 ✗ 표시

## 실행 방식

### 1단계: 현재 설정 상태 확인
```bash
# settings.json에 statusLine 설정 확인
cat ~/.claude/settings.json 2>/dev/null | grep -A3 statusLine || echo "statusLine 설정 없음"

# statusline-command.sh 존재 여부 확인
ls -la ~/.claude/statusline-command.sh 2>/dev/null || echo "스크립트 없음"
```

### 2단계: 사전 요구사항 확인
```bash
# jq 설치 확인
which jq || echo "jq 미설치"

# bc 설치 확인
which bc || echo "bc 미설치"
```

### 3단계: 설치 진행
사용자에게 설치 진행 여부를 확인한 후, 승인 시 다음 스크립트를 실행합니다:

```bash
bash {PLUGIN_PATH}/scripts/setup-statusline.sh
```

### 4단계: 설치 검증
```bash
# 테스트 실행
echo '{"model":{"display_name":"Claude Opus 4.5"},"workspace":{"current_dir":"'$(pwd)'"},"context_window":{"remaining_percentage":40,"used_percentage":60}}' | bash ~/.claude/statusline-command.sh
```

### 5단계: 완료 안내
설치 완료 후 사용자에게 Claude Code 재시작을 안내합니다.

## 문제 해결

### jq 미설치 시
- macOS: `brew install jq`
- Ubuntu/Debian: `sudo apt install jq`

### bc 미설치 시 (Linux)
- Ubuntu/Debian: `sudo apt install bc`
