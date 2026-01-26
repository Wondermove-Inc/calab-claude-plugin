---
name: cli-tools:statusline
description: Claude Code statusline 설치 및 관리. 설치, 롤백 기능을 제공합니다.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# /cli-tools:statusline - Statusline 설치 및 관리

## 설명
Claude Code 터미널에 상태 정보를 표시하는 statusline을 설치하고 관리합니다.

## 사용법
- `/cli-tools:statusline` - 플러그인 statusline 설치 (기존 설정 백업)
- `/cli-tools:statusline 롤백` - 백업에서 이전 설정으로 복원
- `/cli-tools:statusline rollback` - 백업에서 이전 설정으로 복원

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

## 실행 방식

### 사용자 요청 분석
사용자 입력에서 롤백 키워드가 있으면 **롤백 모드**, 그 외에는 **설치 모드**로 실행합니다.

#### 롤백 키워드
다음 키워드 중 하나가 포함되면 롤백 모드:
- 한글: "롤백", "복원", "이전", "되돌"
- 영문: "rollback", "restore"

---

## 설치 모드 (기본)

### 1단계: 현재 상태 확인
```bash
# 현재 설정 확인
cat ~/.claude/settings.json 2>/dev/null | grep -A5 statusLine || echo "statusLine 설정 없음"
ls -la ~/.claude/statusline-command.sh 2>/dev/null || echo "스크립트 없음"

# 기존 백업 목록
ls -dt ~/.claude/backup/statusline_* 2>/dev/null | head -5 || echo "백업 없음"
```

### 2단계: 사전 요구사항 확인
```bash
which jq || echo "jq 미설치"
which bc || echo "bc 미설치"
```

### 3단계: 설치 확인
사용자에게 설치 진행 여부를 확인합니다:
- 기존 설정이 있으면 백업됩니다
- 플러그인 statusline으로 교체됩니다
- 롤백이 필요하면 `/cli-tools:statusline 롤백` 사용

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

## 롤백 모드

### 1단계: 백업 목록 확인
```bash
# 백업 디렉토리 목록 (최신순)
ls -dt ~/.claude/backup/statusline_* 2>/dev/null || echo "백업 없음"
```

### 2단계: 최신 백업 내용 확인
```bash
LATEST_BACKUP=$(ls -dt ~/.claude/backup/statusline_* 2>/dev/null | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    echo "최신 백업: $LATEST_BACKUP"
    ls -la "$LATEST_BACKUP"
fi
```

### 3단계: 복원할 백업 선택
백업이 여러 개인 경우 사용자에게 선택을 요청합니다.

### 4단계: 복원 실행
사용자가 선택한 백업 경로를 `$BACKUP_DIR` 변수에 할당 후 아래 명령을 실행합니다.
(예: `BACKUP_DIR="$LATEST_BACKUP"` 또는 사용자가 직접 선택한 경로)

```bash
# 복원 전 현재 설정 백업 (안전)
PRE_RESTORE=~/.claude/backup/pre_restore_$(date +%Y%m%d_%H%M%S)
mkdir -p "$PRE_RESTORE"
cp ~/.claude/settings.json "$PRE_RESTORE/" 2>/dev/null || true
cp ~/.claude/statusline-command.sh "$PRE_RESTORE/" 2>/dev/null || true
echo "복원 전 백업 완료: $PRE_RESTORE"

# 선택한 백업에서 복원
cp "$BACKUP_DIR/settings.json" ~/.claude/settings.json 2>/dev/null || true
cp "$BACKUP_DIR/statusline-command.sh" ~/.claude/statusline-command.sh 2>/dev/null || true
echo "복원 완료: $BACKUP_DIR"
```

### 5단계: 완료 안내
복원 완료 후 Claude Code 재시작을 안내합니다.

---

## 백업 구조
```
~/.claude/backup/
├── statusline_20260126_143052/      # setup 시 생성
│   ├── settings.json
│   └── statusline-command.sh
├── pre_restore_20260126_150000/     # rollback 시 생성 (안전)
│   ├── settings.json
│   └── statusline-command.sh
```

## 문제 해결

### jq 미설치
- macOS: `brew install jq`
- Ubuntu/Debian: `sudo apt install jq`

### bc 미설치 (Linux)
- Ubuntu/Debian: `sudo apt install bc`
